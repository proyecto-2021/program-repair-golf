from . import python
from .. import db
from flask import request, make_response, jsonify
from .models import PythonChallengeModel
from json import loads
from os import path
import subprocess
from .file_utils import *
from .subprocess_utils import *

@python.route('/login', methods=['GET'])
def login():
    return { 'result': 'ok' }

@python.route('/api/v1/python-challenges', methods=['GET'])
def return_challenges(): 
    #Get all the challanges
    all_challenges = PythonChallengeModel.query.all()
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
    challenge = PythonChallengeModel.query.filter_by(id = id).first()
    
    if challenge is None:
        return make_response(jsonify({"Challenge": "Not found"}), 404)

    #Dictionary auxiliary to modify the keys
    response = PythonChallengeModel.to_dict(challenge)  
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
    new_challenge = PythonChallengeModel(code=new_code_path,
        tests_code=new_tests_path,
        repair_objective=challenge_data['repair_objective'],
        complexity=challenge_data['complexity'],
        best_score=0)

    db.session.add(new_challenge)
    db.session.commit()

    #create response
    req_challenge = PythonChallengeModel.query.filter_by(id=new_challenge.id).first()
    response = PythonChallengeModel.to_dict(req_challenge)
    #adding source codes to response
    response['code'] = challenge_source_code.decode()
    response['tests_code'] = tests_source_code.decode()
    return jsonify({"challenge" : response})


@python.route('api/v1/python-challenges/<id>', methods=['PUT'])
def update_challenge(id):
    challenge_data = request.form.get('challenge')
    if challenge_data != None: challenge_data = loads(challenge_data)['challenge']
    save_to = "public/challenges/"  #general path were code will be saved

    req_challenge = PythonChallengeModel.query.filter_by(id=id).first()

    if req_challenge is None:   #case id is not in database
        return make_response(jsonify({"challenge":"there is no challenge with that id"}),404)

    response = PythonChallengeModel.to_dict(req_challenge).copy()   #start creating response for the endpoint

    new_code = request.files.get('source_code_file')
    new_test = request.files.get('test_suite_file')

    if file_changes_required(challenge_data, new_code, new_test):
        update_result = update_files(challenge_data, new_code, new_test, req_challenge, response)
        if 'Error' in update_result:
            return make_response(jsonify(update_result), 409)

    #check if change for repair objective was requested
    if challenge_data != None:
        if 'repair_objective' in challenge_data:
            response['repair_objective'] = challenge_data['repair_objective']
        #check if change for repair objective was requested
        if 'complexity' in challenge_data:
            response['complexity'] = challenge_data['complexity']
    
    #updating challenge in db with data in response
    db.session.query(PythonChallengeModel).filter_by(id=id).update(dict(response))
    db.session.commit()

    #in case contents of files were changed update 'code' and 'tests_code' keys of response with code
    if new_code != None:    #for some reason new_code (file) cannot be read again
        response['code'] = read_file(response['code'], "r")

    if new_test != None:
        response['tests_code'] = read_file(response['tests_code'], "r")

    return jsonify({"challenge" : response})

#checks for name or content change reuqest
def file_changes_required(names, code, tests):
    return code is None or tests is None or 'source_code_file_name' in names or 'test_suite_file_name' in names

def update_files(names, new_code, new_test, old_paths, response):
    temp_path = "public/temp/"      #path to temp directory

    code_name, test_name = None, None
    if names != None:
        code_name = names.get('source_code_file_name')
        test_name = names.get('test_suite_file_name')

    #saving changes in a temporal location for checking validation
    temp_code_path = save_changes(code_name, new_code, old_paths.code, temp_path)
    temp_test_path = save_changes(test_name, new_test, old_paths.tests_code, temp_path)
    #challenge validation
    validation_result = valid_python_challenge(temp_code_path, temp_test_path)
    if 'Error' in validation_result:
        return validation_result
    #old challenge files deletion
    try:
        delete_file(old_paths.code)
        delete_file(old_paths.tests_code)
    except CalledProcessError as err:
        return {"Error": "Internal Server Error"}
    #new challenge files saving
    new_code_path = "public/challenges/" + (lambda x: x.split('/')[-1]) (temp_code_path)
    save_file(new_code_path, "wb", read_file(temp_code_path, "rb")) #read file in temp and save it in challenges

    new_test_path = "public/challenges/" + (lambda x: x.split('/')[-1]) (temp_test_path)
    save_file(new_test_path, "wb", read_file(temp_test_path, "rb")) #read file in temp and save it in challenges
    
    #deletion of files at temp
    try:
        delete_file(temp_code_path)
        delete_file(temp_test_path)
    except CalledProcessError as err:
        return {"Error": "Internal Server Error"}

    #adding new paths to response (response is used later to save challenge in db)
    response['code'] = new_code_path
    response['tests_code'] = new_test_path
    
    return { 'Result': 'ok' }    

