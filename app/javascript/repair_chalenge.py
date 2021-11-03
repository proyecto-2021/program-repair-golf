from flask import jsonify, make_response,request
from .. import db
import json
import nltk
from .folders_and_files import FILE_JS_EXTENSION
from .models_js import JavascriptChallenge
from .controllers.files_controller import is_file_suffix, exist_file, to_temp_file, upload_file, replace_file, remove_files, open_file
from .modules.source_code_module import compile_js, test_run
from .exceptions.CommandRunException import CommandRunException
from .exceptions.FileUploadException import FileUploadException

def repair_chalenge_js(id):
    try:
        challenge = JavascriptChallenge.query.filter_by(id = id).first()
        code_files_new = request.files['source_code_file']  

        if not challenge:
            return make_response(jsonify({"Error": "challenge is null"},404))

        if not exist_file(challenge.code):
            return make_response(jsonify({"Error": "The path non existent file"},404))

        file_path_new = to_temp_file(challenge.code)  
        upload_file(code_files_new, file_path_new)
        compile_js(file_path_new)
        test_run(challenge.tests_code)

        #? correr el tests, multiplicar el tiempo de ejeccucion *10 y sumarselo al score        

        score = nltk.edit_distance(open_file(challenge.code), open_file(file_path_new))

        if score < challenge.best_score or challenge.best_score == 0:
            replace_file(file_path_new, challenge.code)
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
    
    except CommandRunException as e: 
        remove_files(file_path_new)
        return make_response(jsonify({'Error': e.msg }), e.HTTP_code)
    except FileUploadException as e:
        return make_response(jsonify({'Error': e.msg }), e.HTTP_code)