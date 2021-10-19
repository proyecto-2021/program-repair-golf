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
        challenge_to_return["code"]="".join(from_file_to_str(os.path.abspath(challenge_to_return["code"])))
        del challenge_to_return["id"]
        return jsonify({"challenge":challenge_to_return})


def from_file_to_str(path):
    file= open(str(path),'r')
    content=file.readlines()
    file.close()
    return content