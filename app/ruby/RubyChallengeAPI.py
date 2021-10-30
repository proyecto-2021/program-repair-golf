from flask.views import MethodView
from . import ruby
from .models import *
from flask import jsonify, request, make_response, current_app
from shutil import copy
import json, os
import nltk
from .filemanagement import *
from tempfile import gettempdir

class RubyChallengeAPI(MethodView):

    def __init__(self):
        self.files_path = current_app.config.get('FILES_PATH')

    def post(self, id):
        if id is None:

            dictionary = json.loads(request.form.get('challenge'))['challenge']

            file = request.files['source_code_file']
            file_path = self.files_path + dictionary['source_code_file_name'] + '.rb'

            test_file = request.files['test_suite_file']
            test_file_path = self.files_path + dictionary['test_suite_file_name'] + '.rb'

            #check that the same files is not posted again
            if not save(file, file_path):
                return make_response(jsonify({'challenge': 'source_code is already exist'}),409)

            if not save(test_file, test_file_path):
                remove([file_path])
                return make_response(jsonify({'challenge': 'test_suite is already exist'}),409)

            #check no syntax's errors
            if not (compiles(file_path) and compiles(test_file_path)):
                remove([file_path, test_file_path])
                return make_response(jsonify({'challenge': 'source_code and/or test_suite not compile'}),400)

            if not dependencies_ok(test_file_path, dictionary['source_code_file_name']):
                remove([file_path, test_file_path])
                return make_response(jsonify({'challenge': 'test_suite dependencies are wrong'}),400)

            if not tests_fail(test_file_path):
                remove([file_path, test_file_path])
                return make_response(jsonify({'challenge': 'test_suite does not fail'}),400)

            new_challenge = create_challenge(file_path, test_file_path, dictionary['repair_objective'], dictionary['complexity'])

            new_challenge['code'] = get_content(new_challenge['code'])

            new_challenge['tests_code'] = get_content(new_challenge['tests_code'])

            return jsonify({'challenge': new_challenge})
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
                return make_response(jsonify({'challenge': {'repair_code': 'is erroneous'}}),400)

            test_file_name = gettempdir() + '/repair-zone' + '/tmp_test_file.rb'
            copy(challenge['tests_code'], test_file_name)

            if tests_fail(test_file_name):
                remove([file_name, test_file_name])
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
            challenges = get_challenges()

            for c in challenges:
                delete_keys([c], ['tests_code'])
                c['code'] = get_content(c['code'])

            return jsonify({'challenges': challenges})
        else:
            if not exists(id):
                return make_response(jsonify({'challenge': 'NOT FOUND'}),404)

            challenge = get_challenge(id)
            delete_keys([challenge], ['id'])
            challenge['code'] = get_content(challenge['code'])
            challenge['tests_code'] = get_content(challenge['tests_code'])

            return jsonify({'challenge': challenge})

    def put(self, id):
        if not exists(id):
            return make_response(jsonify({'challenge': 'NOT FOUND'}), 404)
        update_data = json.loads(request.form.get('challenge'))['challenge']
        old_challenge = get_challenge(id)
        source_code_name = f"{update_data['source_code_file_name']}.rb"
        source_test_name = f"{update_data['test_suite_file_name']}.rb"
        source_code_path_destiny = f"{self.files_path}{source_code_name}"
        source_test_path_destiny = f"{self.files_path}{source_test_name}"

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
        update_file(old_challenge, 'code', source_code_path_tmp, self.files_path, source_code_name, update_data)
        update_file(old_challenge, 'tests_code', source_test_path_tmp, self.files_path, source_test_name, update_data)

        # Update challenge with new paths
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