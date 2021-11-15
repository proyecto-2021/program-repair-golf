from flask.views import MethodView
from . import ruby
from flask import request, current_app
from .controller import Controller

class RubyChallengeAPI(MethodView):
    def __init__(self):
        self.files_path = current_app.config.get('FILES_PATH')
        self.controller = Controller(self.files_path)

    def post(self):
        code = request.files.get('source_code_file')
        tests_code = request.files.get('test_suite_file')
        json_challenge = request.form.get('challenge')
        return self.controller.post_challenge(code, tests_code, json_challenge)

    def get(self, id):
        if id is None:
            return self.controller.get_all_challenges()
        else:
            return self.controller.get_challenge(id)

    def put(self, id):
        code = request.files.get('source_code_file')
        tests_code = request.files.get('test_suite_file')
        json_challenge = request.form.get('challenge')
        return self.controller.modify_challenge(id, code, tests_code, json_challenge)
       
class RubyChallengeRepairAPI(MethodView):
    def __init__(self):
        self.files_path = current_app.config.get('FILES_PATH')
        self.controller = Controller(self.files_path)

    def post(self, id):
        repair_candidate = request.files.get('source_code_file')
        return self.controller.post_repair(id, repair_candidate)


ruby_challenge_view = RubyChallengeAPI.as_view('ruby_challenge_api')
ruby_challenge_repair_view = RubyChallengeRepairAPI.as_view('ruby_challenge_repair_api')
ruby.add_url_rule('/challenge', view_func=ruby_challenge_view, methods=['POST',])
ruby.add_url_rule('/challenges', defaults={'id': None}, view_func=ruby_challenge_view, methods=['GET',])
ruby.add_url_rule('/challenge/<int:id>', view_func=ruby_challenge_view, methods=['GET', 'PUT'])
ruby.add_url_rule('/challenge/<int:id>/repair', view_func=ruby_challenge_repair_view, methods=['POST',])