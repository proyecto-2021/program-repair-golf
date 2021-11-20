"""Define views for Ruby endpoints."""
from flask.views import MethodView
from . import ruby
from flask import request, current_app
from .controller import Controller
from flask_jwt import jwt_required, current_identity

class RubyChallengeAPI(MethodView):
    """Provide endpoint views."""
    def __init__(self):
        """Initialize API. 
        
        Attributes:
            files_path (str): set where files are stored,
            controller (Controller): set the object to manage requests.
        """
        self.files_path = current_app.config.get('FILES_PATH')
        self.controller = Controller(self.files_path)

    @jwt_required()
    def post(self):
        """Post a new Challenge"""
        code = request.files.get('source_code_file')
        tests_code = request.files.get('test_suite_file')
        json_challenge = request.form.get('challenge')
        return self.controller.post_challenge(code, tests_code, json_challenge)

    @jwt_required()
    def get(self, id):
        """Get challenge/s
        
        Parameters:
            id (int): id of the challenge to return. Defaults to None to return all challenges.
        """
        if id is None:
            return self.controller.get_all_challenges()
        else:
            return self.controller.get_challenge(id)

    @jwt_required()
    def put(self, id):
        """Modify a challenge
        
        Parameters:
            id (int): id of the challenge to modify.
        """
        code = request.files.get('source_code_file')
        tests_code = request.files.get('test_suite_file')
        json_challenge = request.form.get('challenge')
        return self.controller.modify_challenge(id, code, tests_code, json_challenge)
       
class RubyRepairChallengeAPI(MethodView):
    """Manage repair attempts"""
    def __init__(self):
        """Initialize API. 
        
        Attributes:
            files_path (str): set where files are stored,
            controller (Controller): set the object to manage database.
        """
        self.files_path = current_app.config.get('FILES_PATH')
        self.controller = Controller(self.files_path)

    @jwt_required()
    def post(self, id):
        """Propose a candidate.
        
        Parameters:
            id (int): id of the challenge to repair
        """
        repair_candidate = request.files.get('source_code_file')
        return self.controller.post_repair(id, current_identity, repair_candidate)

ruby_challenge_view = RubyChallengeAPI.as_view('ruby_challenge_api')
ruby_repair_challenge_view = RubyRepairChallengeAPI.as_view('ruby_repair_challenge_api')
ruby.add_url_rule('/challenge', view_func=ruby_challenge_view, methods=['POST',])
ruby.add_url_rule('/challenges', defaults={'id': None}, view_func=ruby_challenge_view, methods=['GET',])
ruby.add_url_rule('/challenge/<int:id>', view_func=ruby_challenge_view, methods=['GET', 'PUT'])
ruby.add_url_rule('/challenge/<int:id>/repair', view_func=ruby_repair_challenge_view, methods=['POST',])