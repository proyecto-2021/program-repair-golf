import os
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

    # Guardo los datos a actualizar
    new_code = f"{request_data['source_code_file_name']}.go"
    new_test_code = f"{request_data['test_suite_file_name']}.go"
    new_repair_objective = request_data['repair_objective']
    new_complexity = request_data['complexity']

    #code_path = "public/challenges/" + f"{new_code}"
    #test_path = "public/challenges/" + f"{new_test_code}" 

    #Nico
    code_path = "example-challenges/go-challenges/" + f"{new_code}"
    test_path = "example-challenges/go-challenges/" + f"{new_test_code}"

    '''if os.path.isfile(code_path) and code_path != challenge['code']:
        make_response({'code':'existing code path'}, 400)
    if os.path.isfile(test_path) and test_path != challenge['test_code']:
        make_response({'test_code':'existing test path'}, 400)'''

    # Controlar que los archivos no tengan errores de sintaxis
    code_compile = subprocess.run(["go", "build" ,code_path],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    test_compile = subprocess.run(["go", "test", "-c"],cwd="public/challenges")
    pass_test_suite = subprocess.run(["go", "test"],cwd="public/challenges")
    
    if code_compile.returncode == 2:
        return make_response(jsonify({"code_file":"code with sintax errors"}),409)
    elif test_compile.returncode == 2:
        return make_response(jsonify({"test_code_file":"test with sintax errors"}),409)
    elif pass_test_suite.returncode == 0:
        return make_response(jsonify({"test_suite":"pass test suite"}),409)

    # Controlar que la suite de pruebas falla
    # Verifico si el test falla 
    if subprocess.run(['go', 'test', '-v'], cwd=test_path.replace(new_test_code,'')).returncode == 0:
        return ({'test_code_file':'test must fails'}, 412)

    # Actualizacion
    challenge.code = code_path
    challenge.tests_code = test_path
    challenge.repair_objetive = new_repair_objective    
    challenge.complexity = new_complexity
    challenge.best_score = 0

    db.session.commit()
    
    #Retorna el codigo fuente de code y la testsuite
    challenge_dict = challenge.convert_dict()
    from_file_to_str(challenge_dict)
    from_file_to_str_tests(challenge_dict)
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