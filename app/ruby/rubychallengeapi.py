from flask.views import MethodView
from . import ruby
from .rubychallengemodel import RubyChallengeModel
from flask import jsonify, request, make_response, current_app
from shutil import copy
import os
from json import loads
import nltk
from .filemanagement import *
from tempfile import gettempdir
from .controller import Controller

class RubyChallengeAPI(MethodView):

    def __init__(self):
        self.files_path = current_app.config.get('FILES_PATH')
        self.controller = Controller(self.files_path)

    def post(self, id):
        if id is None:
            code = request.files['source_code_file']
            tests_code = request.files['test_suite_file']
            json = loads(request.form.get('challenge'))
            return self.controller.post_challenge(code, tests_code, json)
        else:
            if not exists(id):
                return make_response(jsonify({'challenge': 'NOT FOUND'}),404)

            challenge = get_challenge(id)

            file = request.files['source_code_file']
            os.mkdir(gettempdir() + '/repair-zone')
            file_name = gettempdir() + '/repair-zone/' + os.path.basename(challenge['code'])
            save(file, file_name)

            if not compiles(file_name):
                remove([file_name])
                os.rmdir(gettempdir() + '/repair-zone')
                return make_response(jsonify({'challenge': {'repair_code': 'is erroneous'}}),400)

            test_file_name = gettempdir() + '/repair-zone' + '/tmp_test_file.rb'
            copy(challenge['tests_code'], test_file_name)

            if tests_fail(test_file_name):
                remove([file_name, test_file_name])
                os.rmdir(gettempdir() + '/repair-zone')
                return make_response(jsonify({'challenge': {'tests_code': 'fails'}}),200)

            with open(challenge['code']) as f1, open(file_name) as f2:
                score = nltk.edit_distance(f1.read(),f2.read())

            if (score < challenge['best_score']) or (challenge['best_score'] == 0):
                update_challenge(id, {'best_score': score})

            remove([file_name, test_file_name])
            os.rmdir(gettempdir() + '/repair-zone')

            challenge = get_challenge(id)
            delete_keys([challenge], ['id','code','complexity','tests_code'])
            return jsonify( {'repair' :
                                {
                                    'challenge': challenge,
                                    'player': {'username': 'Agustin'},
                                    'attemps': '1',
                                    'score': score
                                }
                            }
                        )

    def get(self, id):
        if id is None:
            return self.controller.get_all_challenges()
        else:
            return self.controller.get_challenge(id)

    def put(self, id):
        code = None
        tests_code = None
        if 'source_code_file' in request.files:
            code = request.files['source_code_file']
        if 'test_suite_file' in request.files:
            tests_code = request.files['test_suite_file']
        json = loads(request.form.get('challenge'))
        return self.controller.modify_challenge(id, code, tests_code, json)
       

ruby_challenge_view = RubyChallengeAPI.as_view('ruby_challenge_api')
ruby.add_url_rule('/challenge', defaults={'id': None}, view_func=ruby_challenge_view, methods=['POST',])
ruby.add_url_rule('/challenges', defaults={'id': None}, view_func=ruby_challenge_view, methods=['GET',])
ruby.add_url_rule('/challenge/<int:id>', view_func=ruby_challenge_view, methods=['GET', 'PUT'])
ruby.add_url_rule('/challenge/<int:id>/repair', view_func=ruby_challenge_view, methods=['POST',])