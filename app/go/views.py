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
    
    try:
        request_data = json.loads(request.form.get('challenge'))['challenge']
    except:
        return make_response(jsonify({'error' : 'bad request'}), 400)

    # Esto es necesario ???
    if request.files:
        if 'source_code_file' in request.files:
            # Y si no nos pasan un nombre pero si los tests ?
            if not ('source_code_file_name' in request_data):
                return make_response(jsonify({'source_code_file_name' : 'doesnt provide it'}), 400)

            new_code_name = request_data['source_code_file_name']
            code_path = f'example-challenges/go-challenges/{new_code_name}'
               
            #if not (os.path.isfile(code_path) and code_path != challenge['code']):
            #if not (os.path.isfile(code_path)):
            new_code_path = f'example-challenges/go-challenges/{new_code_name}.go'

            # Controlo que el nombre del nuevo archivo sea valido
            if (os.path.isfile(new_code_path) and new_code_path != challenge['code']):
                return make_response(jsonify({'challenge' : 'existing code file name'}), 409)
            
            # Esto deberia preguntarse ?
            if not (os.path.isfile(new_code_path)):
                return make_response(jsonify({'source_code_file' : 'not valid'}), 400)

            code_compile = subprocess.run(["go", "build" ,new_code_path],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
            if code_compile.returncode == 2:
                return make_response(jsonify({"code_file":"code with sintax errors"}),409)
                    
            challenge.code = new_code_path
            #challenge['code'] = new_code_path ?
        
        if 'test_suite_file' in request.files:
            # Y si no nos pasan los tests pero si un nombre ?
            if not ('test_suite_file_name' in request_data):
                return make_response(jsonify({'test_suite_file_name' : 'doesnt provide it'}), 400)
                
            new_test_name = request_data['test_suite_file_name']
            test_path = f'example-challenges/go-challenges/{new_test_name}'

            #if not (os.path.isfile(test_path) and test_path != challenge['tests_code']):
            #if not (os.path.isfile(test_path)):
            new_test_path = f'example-challenges/go-challenges/{new_test_name}.go'

            # Controlo que el nombre del nuevo archivo sea valido
            if (os.path.isfile(new_code_path) and new_code_path != challenge['code']):
                return make_response(jsonify({'challenge' : 'existing test suite file name'}), 409)

            # Esto deberia preguntarse ?
            if not (os.path.isfile(new_test_path)):
                return make_response(jsonify({'test_suite_file' : 'not valid'}), 400)
                    
            test_compile = subprocess.run(["go", "test", "-c"],cwd='example-challenges/go-challenges')
                    
            if test_compile.returncode == 1:
                return make_response(jsonify({"test_code_file":"test with sintax errors"}),409)

            pass_test_suite = subprocess.run(['go', 'test'], cwd=test_path.replace(new_test_name,''))
            # Esto reemplaza lo de arriba, pero hay algo que discutir
            #if not compiles(["go", "test", "-c"], 'example-challenges/go-challenges'):
            #    return make_response(jsonify({'test_code_file':'test must fails'}, 412))

                
            if pass_test_suite.returncode == 0:
                return make_response(jsonify({'test_code_file':'test must fails'}), 412)
              
            challenge.tests_code = new_test_path
            #challenge['tests_code'] = new_test_path ?      

    if 'repair_objective' in request_data and request_data['repair_objective'] != challenge.repair_objective:
        challenge.repair_objetive = request_data['repair_objective']

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