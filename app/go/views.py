import json
from flask import Flask,jsonify,request,make_response
from app import db
from . import go
from .models_go import GoChallenge

import shutil
import nltk
import os, subprocess

@go.route('/hello') 
def hello():
    return 'Hello World!'

@go.route('api/v1/go-challenges/<int:id>/repair', methods=['POST'])
def repair_challengue_go(id):
    code_solution_file = request.files['source_code_file']
    subprocess.run(["mkdir","solution"],cwd="public/challenges",stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    code_solution_path = 'public/challenges/solution/code_solution.go'
    code_solution_file.save(code_solution_path)
    
    is_good_code_solution_file = subprocess.run(["go","build",code_solution_path],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)   
    if is_good_code_solution_file.returncode == 2:
        return make_response((jsonify({"code_solution_file":"with errors"}),409))
    
    challengue_original = GoChallenge.query.filter_by(id=id).first()
    if challengue_original is None:
        return make_response(jsonify({'Challenge' : 'this challenge does not exist'}), 404)
    challengue_to_dict = challengue_original.convert_dict()
    tests_code = challengue_to_dict["tests_code"]
    
    shutil.copy (tests_code,"public/challenges/solution/code_test.go")
    
    the_challenge_is_solved = subprocess.run(["go","test"],cwd="public/challenges/solution",stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    if the_challenge_is_solved.returncode == 1:
        return make_response((jsonify({"the challengue":"not solved"}),409))  
    
    challengue_original_code = challengue_to_dict["code"]
    
    f = open (challengue_original_code,'r')
    original_code = f.read()
    f.close()

    f = open (code_solution_path,'r')
    solution_code = f.read()
    f.close()

    edit_distance = nltk.edit_distance(original_code,solution_code)

    current_best_score = challengue_to_dict["best_score"]
    if edit_distance < current_best_score:
        challengue_original.best_score = edit_distance
        db.session.commit()

    challengue_original_updated = GoChallenge.query.filter_by(id=id).first()
    challengue_to_dict_updated = challengue_original_updated.convert_dict()
        

    request_return = {
        "repair":{
            "challenge":{
                "repair_objective": challengue_to_dict["repair_objective"],
                "best_score": challengue_to_dict_updated["best_score"]
            },
            "score": edit_distance
        }
    }

    subprocess.run(["rm","-r","solution"],cwd="public/challenges",stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    
    return jsonify(request_return)

@go.route('/api/v1/go-challenges', methods=['GET'])
def get_all_challenges():
    challenges = db.session.query(GoChallenge).all()
    if not challenges:
        return make_response(jsonify({'challenges' : 'not found'}), 404)
    
    challenges_to_show = []
    i = 0   
    for challenge in challenges:
        challenge_dict = challenge.convert_dict()
        from_file_to_str(challenge_dict, 'code')
        challenges_to_show.append(challenge_dict)
        del challenges_to_show[i]['tests_code']
        i+=1

    return jsonify({"challenges" : challenges_to_show})


@go.route('/api/v1/go-challenges/<id>', methods=['GET'])
def return_single_challenge(id):
    challenge_by_id=GoChallenge.query.filter_by(id=id).first()
    if challenge_by_id is None:
        return "ID Not Found", 404
    challenge_to_return=challenge_by_id.convert_dict()
    from_file_to_str(challenge_to_return, "code")
    from_file_to_str(challenge_to_return, "tests_code")
    del challenge_to_return["id"]
    return jsonify({"challenge":challenge_to_return})

@go.route('/api/v1/go-challenges', methods=['POST'])
def create_go_challenge():
    challenge_data = json.loads(request.form.get('challenge'))['challenge']

    code_file = request.files["source_code_file"]
    code_path = 'public/challenges/' + challenge_data['source_code_file_name']
    code_file.save(code_path)

    test_suite_file = request.files["test_suite_file"]
    test_suite_path = 'public/challenges/' + challenge_data['test_suite_file_name']
    test_suite_file.save(test_suite_path)

    new_challenge = GoChallenge(
        code=code_path,
        tests_code=test_suite_path,
        repair_objective=challenge_data['repair_objective'],
        complexity=challenge_data['complexity'],
        best_score=0)

    all_the_challenges = db.session.query(GoChallenge).all()
    for every_challenge in all_the_challenges:
        if every_challenge.code == new_challenge.code:
            return make_response(jsonify({"challenge": "repeated"}), 409)

    test_pass = subprocess.run(["go", "test"], cwd="public/challenges")
    test_compilation = subprocess.run(["go", "test", "-c"], cwd="public/challenges")
    code_compilation = subprocess.run(["go", "build", code_path], stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)

    if code_compilation.returncode == 2:
        return make_response(jsonify({"code_file": "The code has syntax errors"}), 412)
    elif test_compilation.returncode == 1 or test_compilation.returncode == 2:
        return make_response(jsonify({"test_code_file": "The test code has syntax errors"}), 412)
    elif test_pass.returncode == 0:
        return make_response(jsonify({"ERROR: tests": "There must be at least one test that fails"}), 412)

    db.session.add(new_challenge)
    db.session.commit()

    new_challenge_to_dicc = new_challenge.convert_dict()
    from_file_to_str(new_challenge_to_dicc, "code")
    from_file_to_str(new_challenge_to_dicc, "tests_code")
    return jsonify({"challenge": new_challenge_to_dicc})


def from_file_to_str(challenge, attribute):
    file= open(str(os.path.abspath(challenge[attribute])),'r')
    content=file.readlines()
    file.close()
    challenge[attribute]=content
    return challenge

def compiles(commands, path):
    return (subprocess.run(commands, cwd=path, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL).returncode == 0)

def compiles(command):
    return (subprocess.call(command, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL) == 0)
