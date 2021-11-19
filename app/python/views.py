from . import python
from .. import db
from flask import request, make_response, jsonify
from flask.views import MethodView
from flask_jwt import jwt_required, current_identity
from .models import PythonChallengeModel
from .PythonController import PythonController
from .PythonChallenge import PythonChallenge
from json import loads
from os import path

class PythonViews(MethodView):

    @jwt_required()
    def get(self, id): 
        if id is None:
            challenge_list = PythonController.get_all_challenges()
            return jsonify({"challenges": challenge_list})
        else:
            response = PythonController.get_single_challenge(id)
            if 'Error' in response:
                return make_response(jsonify(response), 409)

            return jsonify({"challenge": response}) 

    @jwt_required()
    def post(self):
        #gather data for post
        try:
            challenge_data = loads(request.form.get('challenge'))['challenge']
            challenge_source_code = request.files.get('source_code_file').read()
            tests_source_code = request.files.get('test_suite_file').read()
        except:
            return make_response(jsonify({'Error' : 'Source code, test code or general data were not provided'}), 409)

        post_result = PythonController.post_challenge(challenge_data, challenge_source_code, tests_source_code)
        if 'Error' in post_result:
            return make_response(jsonify(post_result), 409)

        return jsonify({"challenge": post_result})

    @jwt_required()
    def put(self, id):
        challenge_data = request.form.get('challenge')
        if challenge_data != None: challenge_data = loads(challenge_data)['challenge']
        
        new_code = request.files.get('source_code_file')
        if new_code is not None: new_code = new_code.read()

        new_test = request.files.get('test_suite_file')
        if new_test is not None: new_test = new_test.read()

        update_result = PythonController.put_challenge(id, challenge_data, new_code, new_test)
        if 'Error' in update_result:
            return make_response(jsonify(update_result), 409)

        return jsonify({"challenge" : update_result})

    @jwt_required()
    def repair_challenge(id):
        
        #Repair candidate 
        code_repair = request.files.get('source_code_file')
        user = current_identity
        if code_repair is not None: code_repair = code_repair.read()

        #Result of validated rapair candidate
        repair_result = PythonController.repair_challenge(id, user, code_repair)

        if 'Error' in repair_result:
            return make_response(jsonify(repair_result), 409)

        return jsonify({"repair": repair_result})

python_view = PythonViews.as_view('python_api_crud')
python.add_url_rule('/api/v1/python-challenges', defaults={'id': None}, view_func=python_view, methods=['GET'])
python.add_url_rule('/api/v1/python-challenges', view_func=python_view, methods=['POST'])
python.add_url_rule('/api/v1/python-challenges/<int:id>', view_func=python_view, methods=['GET', 'PUT'])
python.add_url_rule('/api/v1/python-challenges/<int:id>/repair', view_func= PythonViews.repair_challenge, methods=['POST'])
