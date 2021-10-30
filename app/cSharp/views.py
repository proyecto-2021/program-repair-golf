from posixpath import basename
from . import cSharp
from json import loads
from app import db
from .models import CSharp_Challenge
from  flask import jsonify, make_response, json, request
import subprocess, os
from subprocess import PIPE
import nltk

NUNIT_PATH="./app/cSharp/lib/NUnit.3.13.2/lib/net35/"
NUNIT_LIB="./app/cSharp/lib/NUnit.3.13.2/lib/net35/nunit.framework.dll"
NUNIT_CONSOLE_RUNNER="./app/cSharp/lib/NUnit.ConsoleRunner.3.12.0/tools/nunit3-console.exe"
CHALLENGE_SAVE_PATH = "example-challenges/c-sharp-challenges/"
CHALLENGE_VALIDATION_PATH = "./public/challenges/"

@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('/c-sharp-challenges', methods=['POST'])
def post_csharp_challenges():
    #Get new challenge data
    try:
        new_challenge = loads(request.form.get('challenge'))['challenge']
        new_challenge['source_code_file'] = request.files['source_code_file']
        new_challenge['test_suite_file'] = request.files['test_suite_file']
    except:
        return make_response(jsonify({"challenge": "Data not found"}), 404)

    #Validate challenge data
    required_keys = ('source_code_file_name', 'test_suite_file_name', 'source_code_file', 'test_suite_file', 'repair_objective', 'complexity')
    if all (key in new_challenge for key in required_keys):
        new_source_code_path = CHALLENGE_VALIDATION_PATH + new_challenge['source_code_file_name'] + ".cs"
        new_test_suite_path = CHALLENGE_VALIDATION_PATH + new_challenge['test_suite_file_name'] + ".cs"
        new_challenge['source_code_file'].save(new_source_code_path)
        new_challenge['test_suite_file'].save(new_test_suite_path)
        validate_response = validate_challenge(new_source_code_path, new_test_suite_path)
        if validate_response == 0 :
            return make_response(jsonify({'Test': 'At least one has to fail'}), 409)
        elif validate_response == 1 :
            return make_response(jsonify({'Data': 'Valid'}), 200)
        elif validate_response == 2 :
            return make_response(jsonify({'Test': 'Sintax errors'}), 409)
        else:
            return make_response(jsonify({'Challenge': 'Sintax errors'}), 409)
    else:
        return make_response(jsonify({'challenge': 'Data not found'}), 404)
    try:
        os.mkdir(CHALLENGE_SAVE_PATH, new_challenge['source_code_file_name'])
    except FileExistsError:
        return make_response(jsonify({'Challenge': 'Already exists'}), 409)

    #Save validated data
    
    return make_response(jsonify({'Method': 'Not implemented'}), 405)

@cSharp.route('c-sharp-challenges/<int:id>/repair', methods=['POST'])
def repair_Candidate(id):
    # verify challenge's existence 
    if db.session.query(CSharp_Challenge).get(id) is not None:
        challenge = db.session.query(CSharp_Challenge).get(id).__repr__()
        challenge_name = os.path.basename(challenge['code'])
        file = request.files['source_code_file']
        repair_path = 'public/challenges/' + challenge_name
        file.save(dst=repair_path)
        cmd = 'mcs ' + repair_path
        if (subprocess.call(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0):
            test = challenge['tests_code']
            test_dll = test.replace('.cs', '.dll')
            repair_exe_path = repair_path.replace('.cs', '.exe')
            #commands to run tests
            cmd_export = 'export MONO_PATH=' + NUNIT_PATH
            cmd_compile = cmd + ' ' + test + ' -target:library -r:' + NUNIT_LIB + ' -out:' + test_dll
            cmd_execute = 'mono ' + NUNIT_CONSOLE_RUNNER + ' ' + test_dll + ' -noresult'
            cmd_run_test = cmd_export + ' && ' + cmd_compile + ' && ' + cmd_execute 
            if (subprocess.call(cmd_run_test, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0):
                #scoring script
                challenge_script = open(challenge['code'], "r").readlines()
                repair_script = open(repair_path, "r").readlines()
                score = nltk.edit_distance(challenge_script, repair_script)

                if int(challenge['best_score']) == 0 or int(challenge['best_score']) > score:
                    db.session.query(CSharp_Challenge).filter_by(id=id).update(dict(best_score=score))
                    db.session.commit()
                    challenge['best_score'] = score

                challenge_data = {
                    "repair_objective": challenge['repair_objetive'],
                    "best_score": challenge['best_score']
                }
                
                #cleanup
                os.remove(repair_path)
                os.remove(repair_exe_path)
                os.remove(test_dll)
                return make_response(jsonify({'repair': {'challenge': challenge_data, 'score': score}}), 200)
            else:
                #cleanup
                os.remove(repair_path)
                os.remove(repair_exe_path)
                return make_response(jsonify({'Repair candidate:' : 'Tests not passed'}), 409)
        else:
            #cleanup
            os.remove(repair_path)
            return make_response(jsonify({'repair candidate:' : 'Sintax error'}), 409)

    else: 
        return make_response(jsonify({'challenge': 'Not found'}),404)

@cSharp.route('/c-sharp-challenges/<int:id>', methods = ['GET'])
def get_challenge(id):
    if db.session.query(CSharp_Challenge).get(id) is None:
        return make_response(jsonify({'Challenge': 'Not found'}), 404)
    else:
        challenge = db.session.query(CSharp_Challenge).get(id).__repr__()
        challenge['code'] = open(challenge['code'], "r").read()
        challenge['tests_code'] = open(challenge['tests_code'], "r").read()
        return jsonify({ 'Challenge': challenge })

@cSharp.route('/c-sharp-challenges', methods=['GET'])
def get_csharp_challenges():
    challenge = {'challenges': []}
    show = []
    challenge['challenges'] = db.session.query(CSharp_Challenge).all()
    for i in challenge['challenges']:
        show.append(CSharp_Challenge.__repr__(i))
        j = show.index(CSharp_Challenge.__repr__(i))
        show[j]['code'] = open(show[j]['code'], "r").read()
        show[j]['tests_code'] = open(show[j]['tests_code'], "r").read()
    if show != []:
        return jsonify({'challenges': show})
    else:
        return jsonify({'challenges': 'None Loaded'})

def validate_challenge(path_challenge,path_test):
    command ='mcs '+ path_challenge
    if (subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0):
        test_dll= path_test.replace('.cs','.dll')
        cmd_export = 'export MONO_PATH=' + NUNIT_PATH
        cmd_compile = command + ' ' + path_test + ' -target:library -r:' + NUNIT_LIB + ' -out:' + test_dll
        if(subprocess.call(cmd_compile, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0):
            cmd_execute = 'mono ' + NUNIT_CONSOLE_RUNNER + ' ' + test_dll + ' -noresult'
            cmd_run_test = cmd_export + ' && ' + cmd_compile + ' && ' + cmd_execute 
            if subprocess.call(cmd_run_test, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0:
                return 0
            else:
                return 1
        else:
            return 2
    else: 
        return -1