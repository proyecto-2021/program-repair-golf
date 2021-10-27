from flask import jsonify, make_response,request
from .. import db
from .models_js import JavascriptChallenge
from ..javascript import files_js
import json

def update_challenge_js(id):

    challenge_json = json.loads(request.form.get('challenge'))['challenge']
    challenge = JavascriptChallenge.find_challenge(id)
    
    if not challenge_json: return make_response(jsonify({"challenge":"Not found: challenge request is null" }), 404)   
    if not challenge: 
        return make_response(jsonify({"challenge":"Not found: challenge no exits"}), 404) 
    
    source_code_file_upd = request.files['source_code_file']
    test_suite_file_upd = request.files['test_suite_file']
    
    code_file_name = files_js.get_name_file(challenge.code)
    test_file_name = files_js.get_name_file(challenge.tests_code)

    repair_objetive = challenge_json['repair_objective']
    complexity = challenge_json['complexity']

    if files_js.valid(source_code_file_upd):
        challenge.code = files_js.upload(source_code_file_upd, code_file_name)
    if files_js.valid(test_suite_file_upd):
        challenge.tests_code = files_js.upload(test_suite_file_upd, test_file_name)

    compiles_out = files_js.compile_js(challenge.code)
    
    #si los archivos no compomilan tendra un msj de salida y se eliminaran los archivos
    if compiles_out:
        files_js.remove_files(challenge.code,challenge.tests_code)
        return make_response(jsonify({'challenge': f'Error File not compile {compiles_out}'}), 404)
    
    test_out = files_js.run_test(challenge.tests_code)   
    
    #El test devera fallar almenos una vez en caso contrario tendra un msj de salida y se eliminaran los archivos
    if not files_js.test_fail(test_out):
        files_js.remove_files( challenge.code,challenge.tests_code)
        return make_response(jsonify({'challenge': f'The test has to fail at least once {test_out}'}), 404)

    if repair_objetive:
        challenge.repair_objetive = repair_objetive
    if complexity:
        challenge.complexity = complexity

    db.session.commit()
    
    challenge.code = files_js.open_file(challenge.code)
    challenge.tests_code = files_js.open_file(challenge.tests_code)
    return make_response(jsonify({"challenge": challenge.to_dict()}), 200)
