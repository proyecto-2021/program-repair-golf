import os
from typing import ChainMap
from . import go
from flask import request, jsonify, json, make_response
from .. import db
from .models_go import GoChallenge
import subprocess, os

@go.route('/hello') 
def hello():
    return 'Hello World!'


@go.route('/api/v1/go-challenges/<id>', methods=['GET'])
def return_single_challenge(id):
        challenge_by_id=GoChallenge.query.filter_by(id=id).first()
        if challenge_by_id is None:
            return "ID Not Found", 404
        challenge_to_return=challenge_by_id.convert_dict()
        from_file_to_str(challenge_to_return)
        from_file_to_str_tests(challenge_to_return)
        del challenge_to_return["id"]
        return jsonify({"challenge":challenge_to_return})


@go.route('/api/v1/go-challenges/<id>', methods=['PUT'])
def update_a_go_challenge(id):
    challenge = GoChallenge.query.filter_by(id = id).first()
    if challenge is None:
        return jsonify('Challenge not found', 404)
    
    #source_code_file = request.form['source_code_file']
    #test_suite_file  = request.form['test_suite_file']
    #request_data = request.form.get('challenge')
    request_data = json.loads(request.form.get('challenge'))['challenge']

    if request_data is None:
        return make_response(jsonify({"data":"data not found"}),404)

    if request_data['source_code_file_name'] != None:
        new_code = f"{request_data['source_code_file_name']}.go"
        code_path = "example-challenges/go-challenges/" + f"{new_code}"

    if request_data['test_suite_file_name'] != None:
        new_test_code = f"{request_data['test_suite_file_name']}.go"
        test_path = "example-challenges/go-challenges/" + f"{new_test_code}"

    if request_data['repair_objective'] != None:
        new_repair_objective = request_data['repair_objective']

    if request_data['complexity'] != None:
        new_complexity = request_data['complexity']

    #code_path = "public/challenges/" + f"{new_code}"
    #test_path = "public/challenges/" + f"{new_test_code}" 

    # Verifico si los archivos tienen errores de sintaxis y si el test falla 
    change_code = new_code != challenge['code']
    change_test = new_test_code != challenge['tests_code']

    if change_code:
        code_compile = subprocess.run(["go", "build" ,code_path],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
        if code_compile.returncode == 2:
            return make_response(jsonify({"code_file":"code with sintax errors"}),409)

    if change_test:
        test_compile = subprocess.run(["go", "test", "-c"],cwd="public/challenges")
        if test_compile.returncode == 2:
            return make_response(jsonify({"test_code_file":"test with sintax errors"}),409)

    pass_test_suite = subprocess.run(['go', 'test', '-v'], cwd=test_path.replace(new_test_code,''))
    if pass_test_suite.returncode == 0:
        return make_response(jsonify({'test_code_file':'test must fails'}, 412))
    
    ######Nico
    try:
        request_data = json.loads(request.form.get('challenge'))['challenge']
    except:
        return jsonify({'status bad request': 400})

    changes = 0
    if request.files:
        if 'source_code_file' in request.files:
            if not ('source_code_file_name' in request_data):
                return make_response(jsonify({'source_code_file_name' : 'doesnt provide it'}), 400)

            new_code_name = request_data['source_code_file_name']
            code_path = f'example-challenges/go-challenges/{new_code_name}.go'
               
            if not (os.path.isfile(code_path) and code_path != challenge['code']):
                return make_response(jsonify({'source_code_file' : 'not valid'}), 400)

            code_compile = subprocess.run(["go", "build" ,code_path],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
            if code_compile.returncode == 2:
                return make_response(jsonify({"code_file":"code with sintax errors"}),409)
                    
            challenge.code = code_path
            changes += 1
        
        if 'test_suite_file' in request.files:
            if not ('test_suite_file_name' in request_data):
                return make_response(jsonify({'test_suite_file_name' : 'doesnt provide it'}), 400)
                
            new_test_name = request_data['test_suite_file_name']
            test_path = f'example-challenges/go-challenges/{new_test_name}.go'

            if not (os.path.isfile(test_path) and test_path != challenge['tests_code']):
                return make_response(jsonify({'test_suite_file' : 'not valid'}), 400)
                    
            test_compile = subprocess.run(["go", "test", "-c"],cwd='example-challenges/go-challenges')
                    
            if test_compile.returncode == 2:
                return make_response(jsonify({"test_code_file":"test with sintax errors"}),409)
                    
            pass_test_suite = subprocess.run(['go', 'test', '-v'], cwd=test_path.replace(new_test_name+'.go',''))
                
            if pass_test_suite.returncode == 0:
                return make_response(jsonify({'test_code_file':'test must fails'}, 412))
              
            challenge.tests_code = test_path      
            changes += 1


    if 'repair_objective' in request_data and request_data['repair_objective'] != challenge['repair_objective']:
        challenge.repair_objetive = request_data['repair_objective']

    if 'complexity' in request_data and request_data['complexity'] != challenge['complexity']:
        challenge.complexity = request_data['complexity']
    #####
    if changes > 0: 
        challenge.best_score = 0

    db.session.commit()
    
    #Retorna el codigo fuente de code y la testsuite
    challenge_dict = challenge.convert_dict()
    from_file_to_str(challenge_dict)
    from_file_to_str_tests(challenge_dict)
    del challenge_dict['id']
    return jsonify({'challenge': challenge_dict})


def from_file_to_str(challenge):
    file= open(str(os.path.abspath(challenge["code"])),'r')
    content=file.readlines()
    file.close()
    challenge["code"]=(content)
    return challenge


def from_file_to_str_tests(challenge):
    file= open(str(os.path.abspath(challenge["tests_code"])),'r')
    content=file.readlines()
    file.close()
    challenge["tests_code"]=(content)
    return challenge
