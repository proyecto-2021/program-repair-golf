from flask import jsonify, make_response,request
from .. import db
import json
from .folders_and_files import CODES_PATH, FILE_JS_EXTENSION
from .models_js import JavascriptChallenge
from .controllers.files_controller import upload_file, get_name_file, open_file, remove_files
from .modules import source_code_module
from .exceptions.CommandRunException import CommandRunException
from .exceptions.FileUploadException import FileUploadException

def create_challenge_js():
    try:
        data_requ = request.form
        
        if not data_requ:
            return make_response(jsonify({'challenge': 'Data not found'}), 404)
        
        source_code_file = request.files['source_code_file']
        test_suite_file = request.files['test_suite_file']

        challenge_json = json.loads(data_requ.get('challenge'))['challenge']
    
        code_file_name = challenge_json['source_code_file_name'] or get_name_file(source_code_file.file_name)  
        test_file_name = challenge_json['test_suite_file_name'] or get_name_file(test_suite_file.file_name) 
        
        code_file_path = CODES_PATH + code_file_name + FILE_JS_EXTENSION 
        test_file_path = CODES_PATH + test_file_name + FILE_JS_EXTENSION  

        upload_file(source_code_file, code_file_path)
        upload_file(test_suite_file, test_file_path)
        
        source_code_module.compile_js(code_file_path)
        source_code_module.test_fail_run(test_file_path)   
        
        challenge = JavascriptChallenge(code = code_file_path,
                                        tests_code = test_file_path,
                                        repair_objective = challenge_json['repair_objective'],
                                        complexity = challenge_json['complexity'],
                                        best_score = 0)
        
        db.session.add(challenge)
        db.session.commit()

        challenge.code = open_file(challenge.code)
        challenge.tests_code = open_file(challenge.tests_code)

        return make_response(jsonify({"challenge": challenge.to_dict()}), 200)
    
    except CommandRunException as e: 
            remove_files(code_file_path,test_file_path)
            return make_response(jsonify({'Error': e.msg }), e.HTTP_code)
    except FileUploadException as e:
        return make_response(jsonify({'Error': e.msg }), e.HTTP_code)