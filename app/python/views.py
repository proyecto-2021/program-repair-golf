from . import python
from .. import db
from flask import request, make_response, jsonify
from flask.views import MethodView
from .models import PythonChallengeModel
from .PythonController import PythonController
from .PythonChallenge import PythonChallenge
from json import loads
from os import path
from .file_utils import *
from .subprocess_utils import *

class PythonViews(MethodView):

    def get(self, id): 
        if id is None:
            challenge_list = PythonController.get_all_challenges()
            return jsonify({"challenges": challenge_list})
        else:
            response = PythonController.get_single_challenge(id)
            if 'Error' in response:
                return make_response(jsonify(response), 409)

            return jsonify({"Challenge": response}) 

    def post(self):
        #gather data for post
        challenge_data = loads(request.form.get('challenge'))['challenge']
        challenge_source_code = request.files.get('source_code_file').read()
        tests_source_code = request.files.get('test_suite_file').read()

        post_result = PythonController.post_challenge(challenge_data, challenge_source_code, tests_source_code)
        if 'Error' in post_result:
            return make_response(jsonify(post_result), 409)

        return post_result

    def put(self, id):
        challenge_data = request.form.get('challenge')
        if challenge_data != None: challenge_data = loads(challenge_data)['challenge']
        save_to = "public/challenges/"  #general path were code will be saved

        req_challenge = PythonChallengeModel.query.filter_by(id=id).first()

        if req_challenge is None:   #case id is not in database
            return make_response(jsonify({"challenge":"there is no challenge with that id"}),404)

        response = PythonChallengeModel.to_dict(req_challenge).copy()   #start creating response for the endpoint

        new_code = request.files.get('source_code_file')
        new_test = request.files.get('test_suite_file')

        if file_changes_required(challenge_data, new_code, new_test):
            update_result = update_files(challenge_data, new_code, new_test, req_challenge, response)
            if 'Error' in update_result:
                return make_response(jsonify(update_result), 409)

        #check if change for repair objective was requested
        if challenge_data != None:
            if 'repair_objective' in challenge_data:
                response['repair_objective'] = challenge_data['repair_objective']
            #check if change for repair objective was requested
            if 'complexity' in challenge_data:
                response['complexity'] = challenge_data['complexity']
        
        #updating challenge in db with data in response
        db.session.query(PythonChallengeModel).filter_by(id=id).update(dict(response))
        db.session.commit()

        #in case contents of files were changed update 'code' and 'tests_code' keys of response with code
        if new_code != None:    #for some reason new_code (file) cannot be read again
            response['code'] = read_file(response['code'], "r")

        if new_test != None:
            response['tests_code'] = read_file(response['tests_code'], "r")

        return jsonify({"challenge" : response})
    
    #checks for name or content change reuqest
    def file_changes_required(names, code, tests):
        return code is None or tests is None or 'source_code_file_name' in names or 'test_suite_file_name' in names

    def update_files(names, new_code, new_test, old_paths, response):
        temp_path = "public/temp/"      #path to temp directory

        code_name, test_name = None, None
        if names != None:
            code_name = names.get('source_code_file_name')
            test_name = names.get('test_suite_file_name')

        #saving changes in a temporal location for checking validation
        temp_code_path = save_changes(code_name, new_code, old_paths.code, temp_path)
        temp_test_path = save_changes(test_name, new_test, old_paths.tests_code, temp_path)
        #challenge validation
        validation_result = valid_python_challenge(temp_code_path, temp_test_path)
        if 'Error' in validation_result:
            return validation_result
        #old challenge files deletion
        try:
            delete_file(old_paths.code)
            delete_file(old_paths.tests_code)
        except CalledProcessError as err:
            return {"Error": "Internal Server Error"}
        #new challenge files saving
        new_code_path = "public/challenges/" + get_filename(temp_code_path)
        save_file(new_code_path, "wb", read_file(temp_code_path, "rb")) #read file in temp and save it in challenges

        new_test_path = "public/challenges/" + get_filename(temp_test_path)
        save_file(new_test_path, "wb", read_file(temp_test_path, "rb")) #read file in temp and save it in challenges
        
        #deletion of files at temp
        try:
            delete_file(temp_code_path)
            delete_file(temp_test_path)
        except CalledProcessError as err:
            return {"Error": "Internal Server Error"}

        #adding new paths to response (response is used later to save challenge in db)
        response['code'] = new_code_path
        response['tests_code'] = new_test_path
        
        return { 'Result': 'ok' }

python_view = PythonViews.as_view('python_api')
python.add_url_rule('/api/v1/python-challenges', defaults={'id': None}, view_func=python_view, methods=['GET'])
python.add_url_rule('/api/v1/python-challenges', view_func=python_view, methods=['POST'])
python.add_url_rule('/api/v1/python-challenges/<int:id>', view_func=python_view, methods=['GET', 'PUT'])