from flask.views import MethodView
from . import ruby
from .models import *
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
            repair_candidate = request.files['source_code_file']
            return self.controller.post_repair(id, repair_candidate)

    def get(self, id):
        if id is None:
            return self.controller.get_all_challenges()
        else:
            return self.controller.get_challenge(id)

    def put(self, id):
        if not exists(id):
            return make_response(jsonify({'challenge': 'NOT FOUND'}), 404)
        update_data = loads(request.form.get('challenge'))['challenge']
        old_challenge = get_challenge(id)
        source_code_name = f"{update_data['source_code_file_name']}.rb"
        source_test_name = f"{update_data['test_suite_file_name']}.rb"
        source_code_path_destiny = f"{self.files_path}{source_code_name}"
        source_test_path_destiny = f"{self.files_path}{source_test_name}"

        print(source_code_name + source_test_name)

        # Check if file name already exists
        if (file_exists(source_code_path_destiny) and old_challenge['code'] != source_code_path_destiny): 
            return make_response(jsonify({'code': 'code name already exists'}), 400)
        if (file_exists(source_test_path_destiny) and old_challenge['tests_code'] != source_test_path_destiny):
            return make_response(jsonify({'test': 'test name already exists'}), 400)
        del source_code_path_destiny, source_test_path_destiny

        source_code_path_tmp = f"public/{source_code_name}"
        source_test_path_tmp = f"public/{source_test_name}"

        delete_keys([update_data], ['source_code_file_name', 'test_suite_file_name'])

        # If there is a new code file, check if it compiles
        if 'source_code_file' in request.files:
            request.files['source_code_file'].save(dst=source_code_path_tmp)
            if os.path.isfile(source_code_path_tmp) and not compiles(source_code_path_tmp):
                remove([source_code_path_tmp])
                return make_response(jsonify({'code': "doesn't compile or doesn't exists"}), 400)
        else:
            update_file_name(old_challenge, 'code', self.files_path, source_code_name, update_data)

        # If there is a new test suite, check dependencies and if it fails.
        if 'test_suite_file' in request.files:
            request.files['test_suite_file'].save(dst=source_test_path_tmp)
            if os.path.isfile(source_test_path_tmp) and (not compiles(source_test_path_tmp) or not tests_fail(source_test_path_tmp)):
                remove([source_test_path_tmp])
                return make_response(jsonify({'tests': "tests doesn't compiles or doesn't fail"}), 400)
            if not dependencies_ok(source_test_path_tmp, os.path.basename(source_code_name.split('.')[0])):
                remove([source_test_path_tmp])
                return make_response(jsonify({'tests': "dependencies failed to compile"}), 400)
        else:
            if not dependencies_ok(old_challenge['tests_code'], os.path.basename(source_code_name.split('.')[0])):
                remove([source_test_path_tmp])
                return make_response(jsonify({'tests': "dependencies failed to compile"}), 400)
            update_file_name(old_challenge, 'tests_code', self.files_path, source_test_name, update_data)

        #Update DB info (complexity, objective, etc) and remove tmp data in failure case
        if update_challenge(id, update_data) < 1:
            if os.path.isfile(source_test_path_tmp):
                remove([source_test_path_tmp])
            if os.path.isfile(source_code_path_tmp):
                remove([source_code_path_tmp])
            return make_response(jsonify({'challenge': "update failed check input data"}), 400)

        # Update test and code files if they exists
        update_file(old_challenge, 'code', self.files_path, source_code_path_tmp, source_code_name, update_data)
        update_file(old_challenge, 'tests_code', self.files_path, source_test_path_tmp, source_test_name, update_data)

        # Update challenge with new paths
        print(update_data)
        update_challenge(id, update_data)

        # Return updated challenge
        updated_challenge = get_challenge(id)
        delete_keys([updated_challenge], ['id'])
        updated_challenge['code'] = get_content(updated_challenge['code'])
        updated_challenge['tests_code'] = get_content(updated_challenge['tests_code'])
        return jsonify({'challenge': updated_challenge})

ruby_challenge_view = RubyChallengeAPI.as_view('ruby_challenge_api')
ruby.add_url_rule('/challenge', defaults={'id': None}, view_func=ruby_challenge_view, methods=['POST',])
ruby.add_url_rule('/challenges', defaults={'id': None}, view_func=ruby_challenge_view, methods=['GET',])
ruby.add_url_rule('/challenge/<int:id>', view_func=ruby_challenge_view, methods=['GET', 'PUT'])
ruby.add_url_rule('/challenge/<int:id>/repair', view_func=ruby_challenge_view, methods=['POST',])