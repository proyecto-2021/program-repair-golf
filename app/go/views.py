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
        from_file_to_str(challenge_to_return, "code")
        from_file_to_str(challenge_to_return, "tests_code")
        from_file_to_str_tests(challenge_to_return)
        del challenge_to_return["id"]
        return jsonify({"challenge":challenge_to_return})

def from_file_to_str(challenge, attribute):
    file= open(str(os.path.abspath(challenge[attribute])),'r')
    content=file.readlines()
    file.close()
    challenge[attribute]=(content)
    return challenge

def compiles(commands, path):
    return (subprocess.run(commands, cwd=path, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL).returncode == 0)