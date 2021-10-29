from flask import jsonify, make_response,request
from .. import db
from .models_js import JavascriptChallenge
from ..javascript import files_js
import json
import nltk

def repair_chalenge_js(id):
    challenge = JavascriptChallenge.query.filter_by(id = id).first()
    code_files_new = request.files['source_code_file']  
    
    if not files_js.valid(code_files_new): 
        return make_response(jsonify({"Error": "The null or non existent file or must have a .js extension"},404))

    if not challenge:
        return make_response(jsonify({"Error": "challenge is null"},404))

    if not files_js.os.path.lexists(challenge.code):
        return make_response(jsonify({"Error": "The path non existent file"},404))

    file_name = files_js.get_name_file(challenge.code)
    code_files_new_path = files_js.upload(code_files_new, file_name+'_tmp')
    compiles_error_out = files_js.compile_js(code_files_new_path)
    
    if compiles_error_out:
        files_js.remove_files(code_files_new_path)
        return make_response(jsonify({'challenge': f'Error File not compile {compiles_error_out}'}), 404)
    
    score = nltk.edit_distance(files_js.open_file(challenge.code),files_js.open_file(code_files_new_path))

    #? correr el tests, multiplicar el tiempo de ejeccucion *10 y sumarselo al score        

    if score < challenge.best_score or challenge.best_score == 0:
        files_js.remove_files(challenge.code)
        files_js.rename_file(code_files_new_path, file_name)
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