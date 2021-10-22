from . import python
from .. import db
from flask import request, make_response, jsonify
from .models import PythonChallenge
from json import loads
from os import path
import subprocess

@python.route('/login', methods=['GET'])
def login():
    return { 'result': 'ok' }

@python.route('/api/v1/python-challenges', methods=['GET'])
def return_challenges(): 
    all_challenges = PythonChallenge.query.all()
    challenge_list = []
    for challenge in all_challenges:
        
        aux_dict = PythonChallenresponse.to_dict(challenge)
        saved_challenge = open(aux_dict['code'], "r")
        challenge_code = saved_challenge.read()
        aux_dict['code'] = challenge_code
        aux_dict.pop('tests_code', None)
        challenge_list.append(aux_dict)
    return jsonify({"challenges": challenge_list})

@python.route('/api/v1/python-challenges/<id>', methods=['GET'])
def return_challange_id(id):
    challenge = PythonChallenge.query.filter_by(id = id).first()
    if challenge is None:
        return make_response(jsonify({"Challenge": "Not found"}), 404)
    aux_dict = PythonChallenge.to_dict(challenge)  
    saved_challenge = open(aux_dict['code'], "r")   
    challenge_code = saved_challenge.read()
    saved_challenge.close()
    aux_dict['code'] = challenge_code
    saved_challenge2 = open(aux_dict['tests_code'], "r")
    challenge_test_code = saved_challenge2.read()
    saved_challenge2.close()
    aux_dict['tests_code'] = challenge_test_code
    aux_dict.pop('id', None)
    return jsonify({"Challenge": aux_dict}) 

@python.route('/api/v1/python-challenges', methods=['POST'])
def create_new_challenge():
    #we get the dict with keys "source_code_file_name", "test_suite_file_name", "repair_objective", "complexity"
    challenge_data = loads(request.form.get('challenge'))['challenge']
    save_to = "public/challenges/"  #general path were code will be saved
    saved_at = "example-challenges/python-challenges/"  #general path were code is saved

    code_path = saved_at + challenge_data['source_code_file_name']
    test_path = saved_at + challenge_data['test_suite_file_name']
    result = valid_python_challenge(code_path, test_path)
    if 'Error' in result:
        return make_response(jsonify(result), 409)

    challenge_source_code = read_and_resave(save_to, 'source_code_file', challenge_data['source_code_file_name'])
    tests_source_code = read_and_resave(save_to, 'test_suite_file', challenge_data['test_suite_file_name'])
   
    #create row for database with the new challenge
    new_challenge = PythonChallenge(code=code_path,
        tests_code=test_path,
        repair_objective=challenge_data['repair_objective'],
        complexity=challenge_data['complexity'],
        best_score=0)

    db.session.add(new_challenge)
    db.session.commit()

    #create response
    req_challenge = PythonChallenge.query.filter_by(id=new_challenge.id).first()
    response = PythonChallenge.to_dict(req_challenge)
    #adding source codes to response
    response['code'] = challenge_source_code.decode()
    response['tests_code'] = tests_source_code.decode()
    return jsonify({"challenge" : response})


@python.route('api/v1/python-challenges/<id>', methods=['PUT'])
def update_challenge(id):
    challenge_data = loads(request.form.get('challenge'))['challenge']
    save_to = "public/challenges/"  #general path were code will be saved
    temp_path = "public/temp/"      #general path to temp directory

    req_challenge = PythonChallenge.query.filter_by(id=id).first()
    
    if req_challenge is None:   #case id is not in database
        return make_response(jsonify({"challenge":"there is no challenge with that id"}),404)

    response = PythonChallenge.to_dict(req_challenge).copy()   #start creating response for the endpoint
    #determine path to temp, user may have requested name change for the file
    code_path = temp_path
    if 'source_code_file_name' in challenge_data:
        code_path += challenge_data['source_code_file_name']
    else:   #concatenate old file name
        code_path += (lambda x: x.split('/')[-1]) (req_challenge.code)
    
    #same as above
    test_path = temp_path
    if 'test_suite_file_name' in challenge_data:
        test_path += challenge_data['test_suite_file_name']
    else:   #concatenate old file name
        test_path += (lambda x: x.split('/')[-1]) (req_challenge.code)

    #check if code change was requested
    challenge_file = request.files.get('source_code_file')  #obtain the binary
    if challenge_file != None:
        challenge_source_code = challenge_file.read()   #read it, and store its content
        saved_challenge = open(req_challenge.code, "wb")   #creating a new file in new location
        saved_challenge.write(challenge_source_code)    #write the binary we got
        saved_challenge.close()
    
    #check if test code change was requested
    tests_file = request.files.get('test_suite_file')
    if tests_file != None:
        tests_source_code = tests_file.read()
        saved_challenge = open(req_challenge.tests_code, "wb")
        saved_challenge.write(challenge_source_code)
        saved_challenge.close()

    #check if change for repair objective was requested
    if 'repair_objective' in challenge_data:
        db.session.query(PythonChallenge).filter_by(id=id).update(dict( repair_objective = challenge_data['repair_objective']))
        db.session.commit()
        response['repair_objective'] = challenge_data['repair_objective']
    #check if change for repair objective was requested
    if 'complexity' in challenge_data:
        db.session.query(PythonChallenge).filter_by(id=id).update(dict( complexity = challenge_data['complexity']))
        db.session.commit()    

    return jsonify({"challenge" : response})


def read_and_resave(save_to, req_key, filename):
    bin_file = request.files.get(req_key)               #obtain the binary
    source_code = bin_file.read()                       #read it, and store its content
    full_path = path.join(save_to, filename)          #save_path + file_name
    new_save = open(full_path, "wb")                    #creating a new file in new location
    new_save.write(source_code)                         #write the binary we got
    new_save.close()                                    #save it
    return source_code


def valid_python_challenge(code_path,test_path):
    #checks for any syntax errors in code
    if not no_syntax_errors(code_path):
        return {"Error": "Syntax error at " + code_path}
    #checks for any syntax errors in tests code
    elif not no_syntax_errors(test_path):
        return {"Error": "Syntax error at " + test_path}
    #checks if at least one test don't pass
    #elif !tests_fail():
    #    return {"Error": "At least one test must fail"}
    else:   #program is fine 
        return { 'Result': 'ok' }

def no_syntax_errors(code_path):
    p = subprocess.call("python -m py_compile " + code_path ,stdout=subprocess.PIPE, shell=True)
    return p == 0   #0 is no syntax errors, 1 is the opposite
