from flask import jsonify, make_response,request
from .. import db
from .models_js import JavascriptChallenge
from ..javascript import files_controller
import json
import nltk
from .folders_and_files import FILE_JS_EXTENSION

def repair_chalenge_js(id):
    challenge = JavascriptChallenge.query.filter_by(id = id).first()
    code_files_new = request.files['source_code_file']  
    
    if not files_controller.is_file_suffix(code_files_new, FILE_JS_EXTENSION): 
        return make_response(jsonify({"Error": "The null or non existent file or must have a .js extension"},404))

    if not challenge:
        return make_response(jsonify({"Error": "challenge is null"},404))

    if not files_controller.exist_file(challenge.code):
        return make_response(jsonify({"Error": "The path non existent file"},404))

    file_path_new = files_controller.to_temp_file(challenge.code)  
    file_path_new = files_controller.upload(code_files_new, file_path_new)
    compiles_error_out = files_controller.compile_js(file_path_new)
    
    if compiles_error_out:
        files_controller.remove_files(file_path_new)
        return make_response(jsonify({'challenge': f'Error File not compile {compiles_error_out}'}), 404)
    
    score = nltk.edit_distance(files_controller.open_file(challenge.code),files_controller.open_file(file_path_new))

    #? correr el tests, multiplicar el tiempo de ejeccucion *10 y sumarselo al score        

    if score < challenge.best_score or challenge.best_score == 0:
        files_controller.rename_file(file_path_new, challenge.code)
        challenge.best_score = score
        db.session.commit()

    challenge_dict = challenge.to_dict()

    for k in ['id','code','complexity','tests_code']:
        del challenge_dict[k]
        
    return make_response(jsonify( {'repair' :{
                            'challenge': challenge_dict,
                            'player': {'username': 'user'},
                            'attemps': '1',
                            'score': score
                        }}, 200))    