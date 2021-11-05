from .rubychallenge import RubyChallenge
from .rubychallengedao import RubyChallengeDAO
from flask import jsonify, make_response
from os import mkdir
from tempfile import gettempdir
from shutil import rmtree

class Controller:
    def __init__(self, files_path):
        self.files_path = files_path
        self.dao = RubyChallengeDAO()

    def post_challenge(self, code_file, tests_code_file, json):
        data = json['challenge']

        challenge = RubyChallenge(data['repair_objective'], data['complexity'])
        challenge.set_code(self.files_path, data['source_code_file_name'], code_file)
        challenge.set_tests_code(self.files_path, data['test_suite_file_name'], tests_code_file)

        if not challenge.save_code():
            return make_response(jsonify({'challenge': 'source_code already exists'}), 409)

        if not challenge.save_tests_code():
            challenge.remove_code()
            return make_response(jsonify({'challenge': 'test_suite already exists'}), 409)

        if not challenge.codes_compile():
            challenge.remove_code()
            challenge.remove_tests_code()
            return make_response(jsonify({'challenge': 'source_code and/or test_suite not compile'}), 400)

        if not challenge.dependencies_ok():
            challenge.remove_code()
            challenge.remove_tests_code()
            return make_response(jsonify({'challenge': 'test_suite dependencies are wrong'}), 400)

        if not challenge.tests_fail():
            challenge.remove_code()
            challenge.remove_tests_code()
            return make_response(jsonify({'challenge': 'test_suite does not fail'}),400)

        response = challenge.get_content()
        response['id'] = self.dao.create_challenge(**challenge.get_content_for_db())

        return jsonify({'challenge': response})

    def get_challenge(self, id):
        challenge = self.dao.get_challenge_data(id)
        return jsonify({'challenge': challenge})

    def get_all_challenges(self):
        challenges = self.dao.get_challenges_data()
        return jsonify({'challenges': challenges})

    def modify_challenge(self, id, code_file, tests_code_file, json):
        if not self.dao.exists(id):
            return make_response(jsonify({'challenge': 'id doesnt exist'}), 404)

        data = {'repair_objective': None, 'complexity': None}
        data.update(json['challenge'])
        challenge = self.dao.get_challenge(id)
        del challenge['best_score']
        old_challenge = RubyChallenge(**challenge)
        new_challenge = RubyChallenge(data['repair_objective'], data['complexity'])
        ruby_tmp = gettempdir() + '/ruby-tmp/'
        mkdir(ruby_tmp)
        #If files names are in the request, set new_code names to them. If not, take old_challenge name.
        nc_code_name = data['source_code_file_name'] if 'source_code_file_name' in data else old_challenge.code.get_file_name()
        nc_test_name = data['test_suite_file_name'] if 'test_suite_file_name' in data else old_challenge.tests_code.get_file_name()
        
        if code_file is not None:
            new_challenge.set_code(ruby_tmp, nc_code_name, code_file)
            new_challenge.save_code()
            if not new_challenge.code_compile():
                rmtree(ruby_tmp)
                return make_response(jsonify({'code': 'code doesnt compile'}), 400)
        else: #If no file is passed, set the old_challenge code as the new one (Needed to check dependencies)
            old_challenge.copy_code(ruby_tmp)
            new_challenge.set_code(ruby_tmp, old_challenge.code.get_file_name())
            new_challenge.rename_code(nc_code_name)
        
        if tests_code_file is not None:
            new_challenge.set_tests_code(ruby_tmp, nc_test_name, tests_code_file)
            new_challenge.save_tests_code()
            if not new_challenge.tests_compile():
                rmtree(ruby_tmp)
                return make_response(jsonify({'tests': 'tests doesnt compile'}), 400)
        else:
            old_challenge.copy_tests_code(ruby_tmp)
            new_challenge.set_tests_code(ruby_tmp, old_challenge.tests_code.get_file_name())
            new_challenge.rename_tests_code(nc_test_name)

        if not new_challenge.dependencies_ok():
            rmtree(ruby_tmp)
            return make_response(jsonify({'challenge': 'test_suite dependencies are wrong'}), 400)

        if not new_challenge.tests_fail():
            rmtree(ruby_tmp)
            return make_response(jsonify({'challenge': 'test_suite does not fail'}),400)

        # Files are ok, copy it to respective directory
        if old_challenge.code.get_file_name() != new_challenge.code.get_file_name():
            if not new_challenge.move_code(self.files_path, names_match=False):
                return make_response(jsonify({'code': 'code file name already exists'}))
            old_challenge.remove_code()
        else:
            new_challenge.move_code(self.files_path)

        if old_challenge.tests_code.get_file_name() != new_challenge.tests_code.get_file_name():
            if not new_challenge.move_tests_code(self.files_path, names_match=False):
                return make_response(jsonify({'tests': 'tests file name already exists'}))
            old_challenge.remove_tests_code()
        else:
            new_challenge.move_tests_code(self.files_path)

        rmtree(ruby_tmp)

        self.dao.update_challenge(id, {key: value for (key, value) in new_challenge.get_content_for_db().items() if value is not None})
        response = self.dao.get_challenge_data(id)
        return jsonify({'challenge': response})
