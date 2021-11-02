from .rubychallenge import RubyChallenge
from .rubychallengedao import RubyChallengeDAO
from flask import jsonify, make_response

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