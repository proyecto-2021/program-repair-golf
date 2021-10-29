from flask import jsonify, make_response,request
from .. import db
from .models_js import JavascriptChallenge
from ..javascript import files_controller
import json
from .folders_and_files import CODES_FOLDER, FILE_JS_EXTENSION

def update_challenge_js(id):

    challenge_json = json.loads(request.form.get('challenge'))['challenge']
    challenge = JavascriptChallenge.find_challenge(id)
    
    if not challenge_json: 
        return make_response(jsonify({"challenge":"Not found: challenge request is null" }), 404)   
    if not challenge: 
        return make_response(jsonify({"challenge":"Not found: challenge no exits"}), 404) 
    
    source_code_file_upd = request.files['source_code_file']
    test_suite_file_upd = request.files['test_suite_file']
    repair_objetive = challenge_json['repair_objective']
    complexity = challenge_json['complexity']
    
    file_code_path_upd = files_controller.to_temp_file(challenge.code)
    file_test_path_upd = files_controller.to_temp_file(challenge.tests_code)
    
    if files_controller.is_file_suffix(source_code_file_upd, FILE_JS_EXTENSION):
        code_path_upd = files_controller.upload(source_code_file_upd,file_test_path_upd)
        compiles_out_err = files_controller.compile_js(file_test_path_upd)    

    if files_controller.is_file_suffix(test_suite_file_upd, FILE_JS_EXTENSION):
        test_path_upd = files_controller.upload(test_suite_file_upd, file_test_path_upd)
        test_out = files_controller.run_test(file_test_path_upd)  

    #si los archivos no compomilan tendra un msj de salida y se eliminaran los archivos
    #El test devera fallar almenos una vez en caso contrario tendra un msj de salida y se eliminaran los archivos    
    if compiles_out_err or not files_controller.test_fail(test_out):
        files_controller.remove_files(code_path_upd, test_path_upd)
        err = f'Error File not compile {compiles_out_err}' if compiles_out_err else f'The test has to fail at least once {test_out}'
        return make_response(jsonify({'challenge': f'Error File not compile {err}'}), 404)

    if files_controller.exist_file(file_code_path_upd):
        files_controller.rename_file(file_code_path_upd, challenge.code)
    
    if files_controller.exist_file(file_test_path_upd):
        files_controller.rename_file(file_test_path_upd, challenge.tests_code)

    if repair_objetive:
        challenge.repair_objetive = repair_objetive
    if complexity:
        challenge.complexity = complexity

    db.session.commit()
    
    challenge.code = files_controller.open_file(challenge.code)
    challenge.tests_code = files_controller.open_file(challenge.tests_code)
    return make_response(jsonify({"challenge": challenge.to_dict()}), 200)
