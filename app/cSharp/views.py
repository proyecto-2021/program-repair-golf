from posixpath import basename
from . import cSharp
from app import db
from .models import CSharp_Challenge
from  flask import jsonify,make_response,json,request
import subprocess,os
from subprocess import PIPE
import nltk

NUNIT_PATH="./app/cSharp/lib/NUnit.3.13.2/lib/net35/"
NUNIT_LIB="./app/cSharp/lib/NUnit.3.13.2/lib/net35/nunit.framework.dll"
NUNIT_CONSOLE_RUNNER="./app/cSharp/lib/NUnit.ConsoleRunner.3.12.0/tools/nunit3-console.exe"


@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }


@cSharp.route('c-sharp-challenges/<int:id>/repair', methods=['POST'])
def repair_Candidate(id):
    # verify challenge's existence 
    if db.session.query(CSharp_Challenge).get(id) is not None:
        challenge = db.session.query(CSharp_Challenge).get(id).__repr__()
        challenge_name = os.path.basename(challenge['code'])
        file = request.files['source_code_file']
        repair_path = 'public/challenges/' + challenge_name
        file.save(dst=repair_path)
        validation_result = validate_repair(challenge['code'],challenge['tests_code'],repair_path)
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
 

def remove_path(path_list):
    for path in path_list:
        os.remove(path)

def validate_repair(path_challenge,path_test,repair_path=None):
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