import os, subprocess
from . import go
from .models_go import GoChallenge
from app import db
from flask import jsonify, make_response, json, request


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

@go.route('/api/v1/go-challenges/<id>', methods=['PUT'])
def update_a_go_challenge(id):
    challenge = GoChallenge.query.filter_by(id = id).first()
    if challenge is None:
        return make_response(jsonify({'Challenge' : 'not found'}), 404)
    
    request_data = json.loads(request.form.get('challenge'))['challenge']

    if 'source_code_file_name' in request_data:
        new_code_name = request_data['source_code_file_name']
        new_code_path = f'example-challenges/go-challenges/{new_code_name}'

        #if (os.path.isfile(new_code_path) and new_code_path != challenge.code):
        #    return make_response(jsonify({'challenge' : 'existing code file name'}), 409) 

        challenge.code = new_code_path

    if 'test_suite_file_name' in request_data:
        new_test_name = request_data['test_suite_file_name']
        new_test_path = f'example-challenges/go-challenges/{new_test_name}'

        #if (os.path.isfile(new_test_path) and new_test_path != challenge.tests_code):
        #    return make_response(jsonify({'challenge' : 'existing test suite file name'}), 409)

        challenge.tests_code = new_test_path

    code_path = str(challenge.code)
    test_path = str(challenge.tests_code)

    change = False
    
    new_code = 'source_code_file' in request.files 
    if new_code:
        file = request.files['source_code_file']
        file.save(code_path)
        code_compile = subprocess.run(["go", "build", code_path],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
        if code_compile.returncode == 2:
            os.remove(code_path)
            return make_response(jsonify({"code_file":"code with sintax errors"}),409)

        change = True
        
    
    new_test = 'test_suite_file' in request.files
    if new_test: 
        file = request.files['test_suite_file']   
        file.save(test_path)
        test_compile = subprocess.run(["go", "test", "-c"],cwd='example-challenges/go-challenges')        
        if test_compile.returncode == 1:
            os.remove(test_path)
            return make_response(jsonify({"test_code_file":"test with sintax errors"}),409)

        change = True
        #challenge.tests_code = content(test_path)

    if change == True:
        pass_test_suite = subprocess.run(['go', 'test'], cwd='example-challenges/go-challenges')
        if pass_test_suite.returncode == 0:
            if new_code: 
                os.remove(code_path)
            if new_test:
                os.remove(test_path)
            return make_response(jsonify({'test_code_file':'test must fails'}), 412)

    if 'repair_objective' in request_data and request_data['repair_objective'] != challenge.repair_objective:
        challenge.repair_objective = request_data['repair_objective']

    if 'complexity' in request_data and request_data['complexity'] != challenge.complexity:
        challenge.complexity = request_data['complexity']

    db.session.commit()
    challenge_dict = challenge.convert_dict()
    from_file_to_str(challenge_dict, 'code')
    from_file_to_str(challenge_dict, 'tests_code')
    del challenge_dict['id']

    return jsonify({'challenge': challenge_dict})
    

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

def content(path):
    f = open(path, 'r')
    return f.read()
