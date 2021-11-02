from posixpath import basename
from . import cSharp
from json import loads
from app import db
from .models import CSharp_Challenge
from models import *
from  flask import jsonify, make_response, json, request
import subprocess, os
from subprocess import PIPE
import nltk
import shutil

NUNIT_PATH="./app/cSharp/lib/NUnit.3.13.2/lib/net35/"
NUNIT_LIB="./app/cSharp/lib/NUnit.3.13.2/lib/net35/nunit.framework.dll"
NUNIT_CONSOLE_RUNNER="./app/cSharp/lib/NUnit.ConsoleRunner.3.12.0/tools/nunit3-console.exe"
CHALLENGE_SAVE_PATH = "example-challenges/c-sharp-challenges/"
CHALLENGE_VALIDATION_PATH = "./public/challenges/"

UPLOAD_FOLDER = "./example-challenges/c-sharp-challenges/"
@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('/c-sharp-challenges/<int:id>', methods=['PUT'])
def put_csharp_challenges():
    update_request = request.files
    challenge = get_challenge(id)
    if not exist(id):
        return make_response(jsonify({"challenge":"There is no challenge for this id"}), 404) 
    files_keys = ("source_code_file", "test_suite_file")
    challenge_name = os.path.basename(challenge['code'])
    test_name = os.path.basename(challenge['tests_code'])
    old_challenge_path = CHALLENGE_SAVE_PATH + challenge_name.replace('.cs','/') + challenge_name
    old_test_path = CHALLENGE_SAVE_PATH + challenge_name.replace('.cs','/') + test_name
    new_challenge_path = CHALLENGE_VALIDATION_PATH + challenge_name
    new_test_path = CHALLENGE_VALIDATION_PATH + test_name
    new_challenge_exe_path = CHALLENGE_VALIDATION_PATH + challenge_name.replace('.cs','.exe')
    new_test_dll_path = CHALLENGE_VALIDATION_PATH + test_name.replace('.cs','.dll')

    if all(key in update_request for key in files_keys):
        new_challenge = update_request['source_code_file'] 
        new_test = update_request['test_suite_file'] 

        new_challenge.save(new_challenge_path)
        new_test.save(new_test_path)

        validation_result = validate_code(new_challenge_path, new_test_path)
        if validation_result == -1:
            remove_path([new_challenge_path, new_test_path])
            return make_response(jsonify({'Source code': 'Sintax errors'}), 409)
        elif validation_result == 0:
            remove_path([new_challenge_path, new_test_path, new_challenge_exe_path, new_test_dll_path])
            return make_response(jsonify({'Challenge': 'Must fail at least one test'}), 409)
        elif validation_result == 2:
            remove_path([new_challenge_path, new_test_path, new_challenge_exe_path])
            return make_response(jsonify({'Test': 'Sintax errors'}), 409)
        else:
            remove_path([new_challenge_exe_path, new_test_dll_path, old_challenge_path, old_test_path])
            shutil.move(new_challenge_path, old_challenge_path)
            shutil.move(new_test_path, old_test_path)

    elif 'source_code_file' in update_request:
        new_challenge = update_request['source_code_file']
        new_challenge.save(new_challenge_path)
        validation_result = validate_code(new_challenge_path, old_test_path)
        if validation_result == -1:
            remove_path([new_challenge_path])
            return make_response(jsonify({'Source code': 'Sintax errors'}), 409)
        elif validation_result == 0:
            remove_path([new_challenge_path, new_challenge_exe_path, old_test_path.replace('.cs', '.dll')])
            return make_response(jsonify({'Challenge': 'Must fail at least one test'}), 409)
        else:
            remove_path([new_challenge_exe_path, old_test_path.replace('.cs', '.dll'), old_challenge_path])
            shutil.move(new_challenge_path, old_challenge_path)

    elif 'test_suite_file' in update_request:
        new_test = update_request['test_suite_file'] 

        new_test.save(new_test_path)

        validation_result = validate_code(old_challenge_path, new_test_path)
        if validation_result == 0:
            remove_path([new_test_path, old_challenge_path.replace('.cs', '.exe'), new_test_dll_path])
            return make_response(jsonify({'Challenge': 'Must fail at least one test'}), 409)
        elif validation_result == 2:
            remove_path([new_test_path, old_challenge_path.replace('.cs', '.exe')])
            return make_response(jsonify({'Test': 'Sintax errors'}), 409)
        else:
            remove_path([new_test_dll_path, old_challenge_path.replace('.cs', '.exe'), old_test_path])
            shutil.move(new_test_path, old_test_path)
    
    if 'repair_objective' in update_request:
        update_challenge_data(id,{'repair_objetive':update_request['repair_objective']})

    if 'complexity' in update_request:
        complexity = int(update_request['complexity'])
        if complexity < 1 or complexity > 5 :
            return make_response(jsonify({'Complexity': 'Must be between 1 and 5'}), 409)
        else:
            update_challenge_data(id,{'complexity': complexity})

    
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
        try:
            os.mkdir(CHALLENGE_SAVE_PATH + new_challenge['source_code_file_name'])
        except FileExistsError:
            return make_response(jsonify({'Challenge': 'Already exists'}), 409)
        new_source_code_path = CHALLENGE_SAVE_PATH + new_challenge['source_code_file_name'] + "/" + new_challenge['source_code_file_name'] + ".cs"
        new_test_suite_path = CHALLENGE_SAVE_PATH + new_challenge['source_code_file_name'] + "/" + new_challenge['test_suite_file_name'] + ".cs"
        save_challenge_files(new_challenge['source_code_file'], new_source_code_path, new_challenge['test_suite_file'], new_test_suite_path)
        validate_response = validate_code(new_source_code_path, new_test_suite_path)
        new_code_exe_path = new_source_code_path.replace('.cs', '.exe')
        new_test_dll_path = new_test_suite_path.replace('.cs', '.dll')
        if validate_response == 0 :
            shutil.rmtree(CHALLENGE_SAVE_PATH + new_challenge['source_code_file_name'])
            return make_response(jsonify({'Test': 'At least one has to fail'}), 409)

        elif validate_response == 1 :
            remove_path([new_code_exe_path, new_test_dll_path])
            new_data_id = save_challenge(new_challenge, new_source_code_path, new_test_suite_path)
            return make_response(jsonify({'challenge': get_challenge(new_data_id, show_files_content = True)}))

        elif validate_response == 2 :
            shutil.rmtree(CHALLENGE_SAVE_PATH + new_challenge['source_code_file_name'])
            return make_response(jsonify({'Test': 'Sintax errors'}), 409)

        else:
            shutil.rmtree(CHALLENGE_SAVE_PATH + new_challenge['source_code_file_name'])
            return make_response(jsonify({'Challenge': 'Sintax errors'}), 409)

    if int(new_challenge['complexity']) < 1 or int(new_challenge['complexity']) > 5 :
        shutil.rmtree(CHALLENGE_SAVE_PATH + new_challenge['source_code_file_name'])
        return make_response(jsonify({'Complexity': 'Must be between 1 and 5'}), 409)

    else:
        return make_response(jsonify({'challenge': 'Data not found'}), 404)

@cSharp.route('c-sharp-challenges/<int:id>/repair', methods=['POST'])
def repair_Candidate(id):
    # verify challenge's existence 
    if exist(id):
        challenge = get_challenge(id)
        challenge_name = os.path.basename(challenge['code'])
        file = request.files['source_code_file']
        repair_path = 'public/challenges/' + challenge_name
        file.save(dst=repair_path)
        validation_result = validate_code(challenge['code'],challenge['tests_code'],repair_path)
        if validation_result == -1:
            remove_path([repair_path])
            return make_response(jsonify({'repair candidate:' : 'Sintax error'}), 409)

        elif validation_result == 1:
            remove_path([repair_path, repair_path.replace('.cs','.exe'),challenge['tests_code'].replace(".cs",".dll")])
            return make_response(jsonify({'Repair candidate:' : 'Tests not passed'}), 409)
        else:
            score = calculate_score(challenge['code'], repair_path)

            if save_best_score(score, challenge['best_score'], id) == 0:
                challenge['best_score'] = score

            challenge_data = {
                "repair_objective": challenge['repair_objetive'],
                "best_score": challenge['best_score']
            }
            remove_path([repair_path, repair_path.replace('.cs','.exe'),challenge['tests_code'].replace(".cs",".dll")])
            return make_response(jsonify({'repair': {'challenge': challenge_data, 'score': score}}), 200)

@cSharp.route('/c-sharp-challenges/<int:id>', methods = ['GET'])
def get_challenge(id):
    if exist(id):
        return jsonify({ 'Challenge': get_challenge(id, show_files_content = True) })       
    else:
        return make_response(jsonify({'Challenge': 'Not found'}), 404)       

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

def remove_path(path_list):
    for path in path_list:
        os.remove(path)

def validate_code(path_challenge,path_test,repair_path=None):
    if repair_path is None:
        command = 'mcs '+ path_challenge
    else:
        command = 'mcs '+ repair_path

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

def calculate_score(challenge_path, repair_candidate_path):
    challenge_script = open(challenge_path, "r").readlines()
    repair_script = open(repair_candidate_path,"r").readlines()
    return nltk.edit_distance(challenge_script, repair_script)

def save_best_score(score, previous_best_score, challenge_id):
    if previous_best_score == 0 or previous_best_score > score:
        db.session.query(CSharp_Challenge).filter_by(id=challenge_id).update(dict(best_score=score))
        db.session.commit()
        return 0
    else: 
        return 1

def save_challenge(challenge_data, source_code_path, test_path):
    new_challenge = CSharp_Challenge(code = source_code_path, tests_code = test_path, repair_objetive = challenge_data['repair_objective'], complexity = int(challenge_data['complexity']), best_score = 0)
    db.session.add(new_challenge)
    db.session.commit()
    return new_challenge.id

def get_challenge_data(id):
    challenge = db.session.query(CSharp_Challenge).get(id).__repr__()
    challenge['code'] = open(challenge['code'], "r").read()
    challenge['tests_code'] = open(challenge['tests_code'], "r").read()
    return challenge

def save_challenge_files(source_code, source_code_path, test_suite, test_suite_path):
    source_code.save(source_code_path)
    test_suite.save(test_suite_path)
    