from flask.views import MethodView
from . import ruby
from flask import request, current_app
from json import loads
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

            repair_candidate = request.files['source_code_file']
            return self.controller.post_repair(id, repair_candidate)

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