from flask import jsonify, make_response,request
from .. import db
import json
from .models_js import JavascriptChallenge
from .folders_and_files import CODES_FOLDER, FILE_JS_EXTENSION
from .controllers.files_controller import to_temp_file, is_file_suffix, upload_file, remove_files, replace_file, exist_file, open_file
from .modules.source_code_module import compile_js, test_fail_run
from .exceptions.CommandRunException import CommandRunException
from .exceptions.FileUploadException import FileUploadException
from .exceptions.FileReplaceException import FileReplaceException

def update_challenge_js(id):
    try: 
        challenge_json = json.loads(request.form.get('challenge'))['challenge']
        challenge = JavascriptChallenge.find_challenge(id)
        
        if not challenge_json: 
            return make_response(jsonify({"challenge":"Not found: challenge request is null" }), 404)   
        if not challenge: 
            return make_response(jsonify({"challenge":"Not found: challenge no exits"}), 404) 
        
        source_code_file_upd = request.files['source_code_file'] or None
        test_suite_file_upd = request.files['test_suite_file'] or None
        repair_objetive = challenge_json['repair_objective'] or None
        complexity = challenge_json['complexity'] or None
        
        file_code_path_upd = to_temp_file(challenge.code)
        file_test_path_upd = to_temp_file(challenge.tests_code)
        
        if source_code_file_upd:
            upload_file(source_code_file_upd,file_code_path_upd)
            compile_js(file_code_path_upd)    
            replace_file(file_code_path_upd, challenge.code)
        if test_suite_file_upd:     
            upload_file(test_suite_file_upd, file_test_path_upd)
            test_fail_run(file_test_path_upd)  
            replace_file(file_test_path_upd, challenge.tests_code)
        
        if repair_objetive:
            challenge.repair_objetive = repair_objetive
        if complexity:
            challenge.complexity = complexity

        db.session.commit()
        
        challenge.code = open_file(challenge.code)
        challenge.tests_code = open_file(challenge.tests_code)
        return make_response(jsonify({"challenge": challenge.to_dict()}), 200)
    except CommandRunException as e: 
        remove_files(file_code_path_upd, file_test_path_upd)
        return make_response(jsonify({'Error': e.msg }), e.HTTP_code)
    except FileUploadException or FileReplaceException as e:
        return make_response(jsonify({'Error': e.msg }), e.HTTP_code)