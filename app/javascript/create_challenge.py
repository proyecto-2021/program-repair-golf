from flask import jsonify, make_response,request
from .. import db
from .models_js import JavascriptChallenge
from ..javascript import files_js
import json

def create_challenge_js():
    data_requ = request.form
    
    if not data_requ:
        return make_response(jsonify({'challenge': 'Data not found'}), 404)
    
    challenge_json = json.loads(data_requ.get('challenge'))['challenge']
    source_code_file = request.files['source_code_file']
    test_suite_file = request.files['test_suite_file']

    code_file_name = challenge_json['source_code_file_name']   
    test_file_name = challenge_json['test_suite_file_name']

    if not files_js.valid(source_code_file) or not files_js.valid(test_suite_file): 
        return make_response(jsonify({"Error": "The null or non existent file or must have a .js extension"}))

    if files_js.exist_file(code_file_name):
        return make_response(jsonify({'challenge': 'File code exists'}), 409)

    if files_js.exist_file(test_file_name):
        return make_response(jsonify({'challenge': 'File test exists'}), 409)

    source_code_file_path = files_js.upload(source_code_file, code_file_name)
    test_code_file_path = files_js.upload(test_suite_file, test_file_name)

    compiles_out = files_js.compile_js(source_code_file_path)
    
    if compiles_out:
        files_js.remove_files(source_code_file_path,test_code_file_path)
        return make_response(jsonify({'challenge': f'Error File not compile {compiles_out}'}), 404)
    
    test_out = files_js.run_test(test_code_file_path)   
    if not files_js.test_fail(test_out):
        files_js.remove_files(source_code_file_path,test_code_file_path)
        return make_response(jsonify({'challenge': f'The test has to fail at least once {test_out}'}), 404)
    
    challenge = JavascriptChallenge(code = source_code_file_path,
                                    tests_code = test_code_file_path,
                                    repair_objective = challenge_json['repair_objective'],
                                    complexity = challenge_json['complexity'],
                                    best_score = 0)
    
    db.session.add(challenge)
    db.session.commit()

    challenge.code = files_js.open_file(challenge.code)
    challenge.tests_code = files_js.open_file(challenge.tests_code)

    return make_response(jsonify({"challenge": challenge.to_dict()}), 200)
    
    