from flask import jsonify, make_response,request
from .. import db
from .models_js import JavascriptChallenge
from ..javascript import files_controller
from ..javascript import models_js
import json
from .folders_and_files import CODES_PATH, FILE_JS_EXTENSION

def create_challenge_js():
    data_requ = request.form
    
    if not data_requ:
        return make_response(jsonify({'challenge': 'Data not found'}), 404)
    
    source_code_file = request.files['source_code_file']
    test_suite_file = request.files['test_suite_file']

    challenge_json = json.loads(data_requ.get('challenge'))['challenge']
   
    if not (files_controller.is_file_suffix(source_code_file, FILE_JS_EXTENSION) or files_controller.is_file_suffix(test_suite_file, FILE_JS_EXTENSION)): 
        return make_response(jsonify({"Error": "The null or non existent file or must have a .js extension"}), 404)

    code_file_name = challenge_json['source_code_file_name'] or files_controller.get_name_file(source_code_file.file_name)  
    test_file_name = challenge_json['test_suite_file_name'] or files_controller.get_name_file(test_suite_file.file_name) 
    
    code_file_path = CODES_PATH + code_file_name + FILE_JS_EXTENSION 
    test_file_path = CODES_PATH + test_file_name + FILE_JS_EXTENSION  

    if files_controller.exist_file(code_file_path):
        return make_response(jsonify({'challenge': 'File code exists'}), 409)

    if files_controller.exist_file(test_file_path):
        return make_response(jsonify({'challenge': 'File test exists'}), 409)

    files_controller.upload(source_code_file, code_file_path)
    files_controller.upload(test_suite_file, test_file_path)

    # models_js.compileRunTest(code_file_path, test_file_path)

    """
    compiles_out = files_controller.compile_js(code_file_path)
    
    if compiles_out:
        files_controller.remove_files(code_file_path,test_file_path)
        return make_response(jsonify({'challenge': f'Error File not compile {compiles_out}'}), 404)
    
    test_out = files_controller.run_test(test_file_path)   
    if not files_controller.test_fail(test_out):
        files_controller.remove_files(code_file_path,test_file_path)
        return make_response(jsonify({'challenge': f'The test has to fail at least once {test_out}'}), 404)
    
    """
    challenge = JavascriptChallenge(code = code_file_path,
                                    tests_code = test_file_path,
                                    repair_objective = challenge_json['repair_objective'],
                                    complexity = challenge_json['complexity'],
                                    best_score = 0)
    
    db.session.add(challenge)
    db.session.commit()

    challenge.code = files_controller.open_file(challenge.code)
    challenge.tests_code = files_controller.open_file(challenge.tests_code)

    return make_response(jsonify({"challenge": challenge.to_dict()}), 200)