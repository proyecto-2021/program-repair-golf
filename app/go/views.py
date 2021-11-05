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
        new_code_path = f'example-challenges/go-challenges/tmp/{new_code_name}'  

        f = request.files['source_code_file']
        f.save(new_code_path)

        code_compile = subprocess.run(["go", "build", new_code_path],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
        if code_compile.returncode == 2:
            return make_response(jsonify({"code_file":"code with sintax errors"}),409)           

        change = True
        
    new_test = 'test_suite_file' in request.files
    if new_test: 
        if not ('test_suite_file_name' in request_data):
            return make_response(jsonify({'file name' : 'conflict'}),409)
        
        new_test_name = request_data['test_suite_file_name']
        new_test_path = f'example-challenges/go-challenges/tmp/{new_test_name}'

        g = request.files['test_suite_file']   
        g.save(new_test_path)

        test_compile = subprocess.run(["go", "test", "-c"],cwd='example-challenges/go-challenges/tmp/')        
        if test_compile.returncode == 1:
            return make_response(jsonify({"test_code_file":"test with sintax errors"}),409)

        change = True

    if change:
        pass_test_suite = subprocess.run(['go', 'test'], cwd='example-challenges/go-challenges/tmp/')
        if pass_test_suite.returncode == 0:
            os.remove(new_code_path)
            os.remove(new_test_path)
            return make_response(jsonify({'test_code_file':'test must fails'}), 412)

    if new_code:
        with open(new_code_path) as source_code_file:
            with open(old_code_path, 'w') as updateable_file:
                for line in source_code_file:
                    updateable_file.write(line)
                
        os.remove(new_code_path)

    if new_test:
        with open(new_test_path) as test_suite_file:
            with open(old_test_path, 'w') as updateable_file:
                for line in test_suite_file:
                    updateable_file.write(line)
        
        os.remove(new_test_path)
    
    #delete all files 
    #no es eficiente si la carpeta tmp tiene subdirectorios, pero ese caso no creo que ocurra
    for file in os.listdir('example-challenges/go-challenges/tmp/'):
        os.remove(os.path.join('example-challenges/go-challenges/tmp/', file))

    #ver que tenemos guardado en la carpeta temporal:
    # si solo esta source_code_file, agregar la test_suite vieja
    # si solo esta test_suite_file, agregar source_code file viejo
    # otro caso, cambio ambos archivos
    #if change and (new_code and not new_test):


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
