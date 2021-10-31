from .rubychallenge import RubyChallenge
from .rubycode import RubyCode
from .rubychallengedao import RubyChallengeDAO
from flask import jsonify
import json

class Controller:
    def __init__(self, files_path):
        self.files_path = files_path
        self.dao = RubyChallengeDAO()

    def post_challenge(self, request):
        data = json.loads(request.form.get('challenge'))['challenge']
        code = RubyCode(self.files_path, data['source_code_file_name'], request.files['source_code_file'])
        tests_code = RubyCode(self.files_path, data['test_suite_file_name'], request.files['test_suite_file'])

        code.save()
        tests_code.save()

        data = self.dao.create_challenge(code.get_full_name(), tests_code.get_full_name(), data['repair_objective'], data['complexity'])
        challenge = RubyChallenge(data['id'], code, tests_code, data['repair_objective'], data['complexity'], data['best_score'])

        return jsonify({'challenge': challenge.get_content()})