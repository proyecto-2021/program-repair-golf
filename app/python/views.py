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
    #Get all the challanges
    all_challenges = PythonChallenge.query.all()
    challenge_list = [] 
    for challenge in all_challenges:
        #Get row as a dictionary
        response = PythonChallenresponse.to_dict(challenge)
        #Get code from file
        response['code'] = read_file(response['code'], "r")
        response.pop('tests_code', None)
        challenge_list.append(response)

    return jsonify({"challenges": challenge_list})

@python.route('/api/v1/python-challenges/<id>', methods=['GET'])
def return_challange_id(id):
    #Get challenge with given id 
    challenge = PythonChallenge.query.filter_by(id = id).first()
    
    if challenge is None:
        return make_response(jsonify({"Challenge": "Not found"}), 404)

    #Dictionary auxiliary to modify the keys
    aux_dict = PythonChallenge.to_dict(challenge)  
    #Get tests code from file
    response['code'] = read_file(response['code'], "r")
    response['tests_code'] = read_file(response['tests_code'], "r")
    response.pop('id', None)

    return jsonify({"Challenge": response}) 

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
    req_challenge = PythonChallenge.query.filter_by(id=id).first()
    
    if req_challenge is None:   #case id is not in database
        return make_response(jsonify({"challenge":"there is no challenge with that id"}),404)

    response = PythonChallenge.to_dict(req_challenge).copy()   #start creating response for the endpoint
    
    new_code = request.files.get('source_code_file')
    new_test = request.files.get('test_suite_file')
    if file_changes_required(challenge_data, new_code, new_test):
        temporary_save(challenge_data, new_code, new_test, req_challenge.code, req_challenge.tests_code)

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
    save_file(full_path, "wb", source_code)
    return source_code


def valid_python_challenge(code_path,test_path):
    #checks for any syntax errors in code
    if not no_syntax_errors(code_path):
        return {"Error": "Syntax error at " + code_path}
    #checks for any syntax errors in tests code
    elif not no_syntax_errors(test_path):
        return {"Error": "Syntax error at " + test_path}
    #checks if at least one test don't pass
    elif not tests_fail(test_path):
        return {"Error": "At least one test must fail"}
    else:   #program is fine 
        return { 'Result': 'ok' }

def no_syntax_errors(code_path):
    p = subprocess.call("python -m py_compile " + code_path ,stdout=subprocess.PIPE, shell=True)
    return p == 0   #0 is no syntax errors, 1 is the opposite

def  tests_fail(test_path):
    p = subprocess.call("python -m pytest " + test_path ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return p == 1 #1 is exception due a test fail, 0 the oposite
  
#checks for name or content change reuqest
def file_changes_required(names, code, tests):
    return code is None or tests is None or 'source_code_file_name' in names or 'test_suite_file_name' in names

def temporary_save(names, code_file, tests_file, old_code_path, old_test_path):
    temp_path = "public/temp/"      #path to temp directory
    
    code_path = determine_path(names.get('source_code_file_name'), temp_path, old_code_path)
    test_path = determine_path(names.get('test_suite_file_name'), temp_path, old_test_path)

    source_code = None
    if code_file != None:
        source_code = code_file.read()   #read it, and store its content
    else:
        source_code = read_file(old_code_path, "rb")
    save_file(code_path, "wb", source_code)

    source_code_tests = None
    if tests_file != None:
        source_code_tests = tests_file.read()   #read it, and store its content
    else:
        source_code_tests = read_file(old_test_path, "rb")
    save_file(test_path, "wb", source_code_tests)
    

def read_file(path, mode):
    file = open(path, mode)
    content = file.read()
    file.close()
    return content

def save_file(path, mode, content):
    file = open(path, mode)
    file.write(content)
    file.close()

#returns a new path, if no filename, takes an old name from a path
def determine_path(filename, base_path, old_path):
    if filename is None:
        return base_path + (lambda x: x.split('/')[-1]) (old_path)
    else:
        return base_path + filename
