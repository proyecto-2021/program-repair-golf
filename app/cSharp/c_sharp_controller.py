from posixpath import basename
from .c_sharp_challenge import CSharpChallenge
from .c_sharp_repair_candidate import CSharpRepairCandidate
from .c_sharp_challenge_DAO import CSharpChallengeDAO
from json import loads
from flask import jsonify, make_response, json, request
import os

class CSharpController:

    DAO = CSharpChallengeDAO()

    def __init__(self):
        pass

    def get_challenge(self, id):
        if self.DAO.exist(id):
            return jsonify({'Challenge': self.DAO.get_challenge_db(id, show_files_content=True)})
        else:
            return make_response(jsonify({'Challenge': 'Not found'}), 404)