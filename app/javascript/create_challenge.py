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
    source_code_file_path = files_js.upload(source_code_file, challenge_json['source_code_file_name'])
    test_code_file_path = files_js.upload(test_suite_file, challenge_json['test_suite_file_name'])
    
    if not files_js.valid(source_code_file) or not files_js.valid(test_suite_file): 
        return make_response(jsonify({"Error": "The null or nonexistent file or must have a .js extension"}))
    
    challenge = JavascriptChallenge(code = source_code_file_path,
                                    tests_code = test_code_file_path,
                                    repair_objective = challenge_json['repair_objective'],
                                    complexity = challenge_json['complexity'],
                                    best_score = 0)
    
    db.session.add(challenge)
    db.session.commit()
    
    return make_response(jsonify({'challenge': challenge}), 200)