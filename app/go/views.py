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
        return make_response(jsonify({'challenge' : 'not found'}), 404)
    
    old_code_path = challenge.code
    old_test_path = challenge.tests_code

    request_data = json.loads(request.form.get('challenge'))['challenge']

    change = False
    
    new_code = 'source_code_file' in request.files 
    if new_code:
        if not ('source_code_file_name' in request_data):
            return make_response(jsonify({'file name' : 'conflict'}), 409)

        new_code_name = request_data['source_code_file_name']
        new_code_path = f'example-challenges/go-challenges/{new_code_name}'  

        code_compile = subprocess.run(["go", "build", new_code_path],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
        if code_compile.returncode == 2:
            return make_response(jsonify({"code_file":"code with sintax errors"}),409)  

        file = request.files['source_code_file']
        file.save(old_code_path)          

        change = True
        
    new_test = 'test_suite_file' in request.files
    if new_test: 
        if not ('test_suite_file_name' in request_data):
            return make_response(jsonify({'file name' : 'conflict'}),409)
        
        new_test_name = request_data['test_suite_file_name']
        new_test_path = f'example-challenges/go-challenges/{new_test_name}'

        test_compile = subprocess.run(["go", "test", "-c"],cwd='example-challenges/go-challenges')        
        if test_compile.returncode == 1:
            return make_response(jsonify({"test_code_file":"test with sintax errors"}),409)

        file = request.files['test_suite_file']   
        file.save(old_test_path)

        change = True

    if change == True:
        pass_test_suite = subprocess.run(['go', 'test'], cwd='example-challenges/go-challenges')
        if pass_test_suite.returncode == 0:
            if new_code: 
                os.remove(old_code_path)
            if new_test:
                os.remove(old_test_path)
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
