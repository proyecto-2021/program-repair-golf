from .rubychallenge import RubyChallenge
from .rubychallengedao import RubyChallengeDAO
from flask import jsonify, make_response
from os import mkdir, path, rmdir
from tempfile import gettempdir

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
        data = {'repair_objective': None, 'complexity': None}
        data.update(json['challenge'])
        challenge = self.dao.get_challenge(id)
        del challenge['best_score']
        old_challenge = RubyChallenge(**challenge)
        new_challenge = RubyChallenge(data['repair_objective'], data['complexity'])
        ruby_tmp = gettempdir() + '/ruby-tmp/'
        mkdir(ruby_tmp)

        if code_file:
            new_challenge.set_code(ruby_tmp, data['source_code_file_name'], code_file)
            if not new_challenge.save_code():
                return make_response(jsonify({'code': 'couldnt save code'}), 400)
        else:
            new_challenge.set_code(self.files_path, data['source_code_file_name'], None)
            old_challenge.rename_code(data['source_code_file_name'])
        
        if tests_code_file:
            new_challenge.set_tests_code(ruby_tmp, data['test_suite_file_name'], tests_code_file)
            if not new_challenge.save_tests_code():
                new_challenge.remove_code()
                return make_response(jsonify({'test': 'couldnt save tests'}), 400)
        else:
            new_challenge.set_tests_code(self.files_path, data['test_suite_file_name'], None)
            old_challenge.rename_tests_code(data['test_suite_file_name'])
        
        if not new_challenge.codes_compile():
            new_challenge.remove_code()
            new_challenge.remove_tests_code()
            rmdir(ruby_tmp)
            return make_response(jsonify({'challenge': 'source_code and/or test_suite not compile'}), 400)

        if not new_challenge.dependencies_ok():
            new_challenge.remove_code()
            new_challenge.remove_tests_code()
            rmdir(ruby_tmp)
            return make_response(jsonify({'challenge': 'test_suite dependencies are wrong'}), 400)

        if not new_challenge.tests_fail():
            new_challenge.remove_code()
            new_challenge.remove_tests_code()
            rmdir(ruby_tmp)
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
        
        rmdir(ruby_tmp)

        self.dao.update_challenge(id, {key: value for (key, value) in new_challenge.get_content_for_db().items() if value is not None})
        response = self.dao.get_challenge(id)
        return jsonify({'challenge': response})
