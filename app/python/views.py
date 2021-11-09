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
import nltk

class PythonViews(MethodView):

    def get(self, id): 
        if id is None:
            challenge_list = PythonController.get_all_challenges()
            return jsonify({"challenges": challenge_list})
        else:
            response = PythonController.get_single_challenge(id)
            if 'Error' in response:
                return make_response(jsonify(response), 409)

            return jsonify({"challenge": response}) 

    def post(self):
        #gather data for post
        challenge_data = loads(request.form.get('challenge'))['challenge']
        challenge_source_code = request.files.get('source_code_file').read()
        tests_source_code = request.files.get('test_suite_file').read()

        post_result = PythonController.post_challenge(challenge_data, challenge_source_code, tests_source_code)
        if 'Error' in post_result:
            return make_response(jsonify(post_result), 409)

        return jsonify({"challenge": post_result})

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

    def repair_challenge(id):
        #Repair candidate 
        code_repair = request.files.get('source_code_file').read()
        #Result of validated rapair candidate
        repair_result = PythonController.repair_challenge(id, code_repair)

        if 'Error' in result:
            return make_response(jsonify(repair_result), 409)

        return jsonify({"repair": repair_result})

python_view = PythonViews.as_view('python_api')
python.add_url_rule('/api/v1/python-challenges', defaults={'id': None}, view_func=python_view, methods=['GET'])
python.add_url_rule('/api/v1/python-challenges', view_func=python_view, methods=['POST'])
python.add_url_rule('/api/v1/python-challenges/<int:id>', view_func=python_view, methods=['GET', 'PUT'])
python.add_url_rule('/api/v1/python-challenges/<int:id>/repair', view_func=python_view, methods=['POST'])