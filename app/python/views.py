from . import python
from .. import db
from flask import request, make_response, jsonify
from .models import PythonChallenge
from json import loads
from os import path
import subprocess
from .file_utils import *

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
    response = PythonChallenge.to_dict(challenge)  
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
    #save in new path
    challenge_source_code = request.files.get('source_code_file').read()
    new_code_path = save_to + challenge_data['source_code_file_name']
    save_file(new_code_path, "wb", challenge_source_code)
    #save in new path
    tests_source_code = request.files.get('test_suite_file').read()
    new_tests_path = save_to + challenge_data['test_suite_file_name']
    save_file(new_tests_path, "wb", tests_source_code)
   
    #create row for database with the new challenge
    new_challenge = PythonChallenge(code=new_code_path,
        tests_code=new_tests_path,
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
    temp_path = "public/temp/"      #path to temp directory

    req_challenge = PythonChallenge.query.filter_by(id=id).first()

    if req_challenge is None:   #case id is not in database
        return make_response(jsonify({"challenge":"there is no challenge with that id"}),404)

    response = PythonChallenge.to_dict(req_challenge).copy()   #start creating response for the endpoint

    new_code = request.files.get('source_code_file')
    new_test = request.files.get('test_suite_file')
    
    if file_changes_required(challenge_data, new_code, new_test):
        update_result = update_files(challenge_data, new_code, new_test, temp_path, response)
        if 'Error' in update_result:
            return make_response(jsonify(update_result), 409)
    
    #check if change for repair objective was requested
    if 'repair_objective' in challenge_data:
        response['repair_objective'] = challenge_data['repair_objective']
    #check if change for repair objective was requested
    if 'complexity' in challenge_data:
        response['complexity'] = challenge_data['complexity']
    
    #updating challenge in db with data in response
    db.session.query(PythonChallenge).filter_by(id=id).update(dict(response))
    db.session.commit()

    #in case contents of files were changed update 'code' and 'tests_code' keys of response with code
    if new_code != None:    #for some reason new_code is unnabled to read the file again
        print("\ncontent changes won't be shown until we save new path in response['code']\n")
        response['code'] = read_file(response['code'], "r")

    if new_test != None:
        print("\ncontent changes won't be shown until we save new path in response['tests_code']\n")
        response['tests_code'] = read_file(response['tests_code'], "r")

    return jsonify({"challenge" : response})

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
    try:
    p = subprocess.call("python -m py_compile " + code_path ,stdout=subprocess.PIPE, shell=True)
    return p == 0   #0 is no syntax errors, 1 is the opposite
    except CalledProcessError as err:
        return False

def  tests_fail(test_path):
    try:
    p = subprocess.call("python -m pytest " + test_path ,stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        return p != 0 #0 means all tests passed, other value means some test/s failed
    except CalledProcessError as err:
        return True
  
#checks for name or content change reuqest
def file_changes_required(names, code, tests):
    return code is None or tests is None or 'source_code_file_name' in names or 'test_suite_file_name' in names

def update_files(challenge_data, new_code, new_test, temp_path, response):
    #saving changes in a temporal location for checking validation
    temp_code_path = save_changes(challenge_data.get('source_code_file_name'), new_code, req_challenge.code, temp_path)
    temp_test_path = save_changes(challenge_data.get('test_suite_file_name'), new_test, req_challenge.tests_code, temp_path)

    #challenge validation here
    validation_result = valid_python_challenge(temp_code_path, temp_test_path)
    if 'Error' in validation_result:
        return validation_result
    #old challenge files deletion

    #new challenge files saving

    #deletion of files at temp

    #adding new paths to response (response is used later to save challenge in db)
    
    return { 'Result': 'ok' }    

#saves a file with new name and new content
#if not a new name it uses the old one, same for content
def save_changes(new_name, file_content, old_file_path, base_path):
	new_path = determine_path(new_name, base_path, old_file_path)
	#gets new or old content
	source_code = determine_content(file_content, old_file_path)
	save_file(new_path, "wb", source_code)
	return new_path