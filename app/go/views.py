import os
from . import go
from flask import request, jsonify
from .. import db
from .models_go import GoChallenge

@go.route('/hello') 
def hello():
    return 'Hello World!'

@go.route('/api/v1/go-challenges/<id>', methods=['GET'])
def return_single_challenge(id):
        challenge_by_id=GoChallenge.query.filter_by(id=id).first()
        if challenge_by_id is None:
            return "ID Not Found", 404
        challenge_to_return=challenge_by_id.convert_dict()
        from_file_to_str(challenge_to_return)
        from_file_to_str_tests(challenge_to_return)
        del challenge_to_return["id"]
        return jsonify({"challenge":challenge_to_return})


def from_file_to_str(challenge):
    file= open(str(os.path.abspath(challenge["code"])),'r')
    content=file.readlines()
    file.close()
    challenge["code"]=(content)
    return challenge

def from_file_to_str_tests(challenge):
    file= open(str(os.path.abspath(challenge["tests_code"])),'r')
    content=file.readlines()
    file.close()
    challenge["tests_code"]=(content)
    return challenge