import os
from . import go
from .models_go import GoChallenge
from app import db
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
'''from sqlalchemy import create_engine'''
import json


@go.route('/hello') 
def hello():
    return 'Hello World!'


@go.route('/api/v1/go-challenges', methods=['GET'])
def get_all_challenges():
    challenges = db.session.query(GoChallenge).all()
    show = []
    i = 0
    for challenge in challenges:
        challenge_dict = challenge.convert_dict()
        from_file_to_str(challenge_dict)
        show.append(challenge_dict)
        del show[i]['tests_code']
        i+=1
    return jsonify({"challenges" : show})


@go.route('/api/v1/go-challenges/<id>', methods=['GET'])
def return_single_challenge(id):
    challenge_by_id=GoChallenge.query.filter_by(id=id).first()
    if challenge_by_id is None:
        return "ID Not Found", 404
    challenge_to_return=challenge_by_id.convert_dict()
    from_file_to_str(challenge_to_return)
    del challenge_to_return["id"]
    return jsonify({"challenge":challenge_to_return})


def from_file_to_str(challenge):
    file= open(str(os.path.abspath(challenge["code"])),'r')
    content=file.readlines()
    file.close()
    challenge["code"]="".join(content)
    return challenge

