from . import go
from .models_go import GoChallenge
from app import db
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
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
		show.append(GoChallenge.convert_dict(challenge))
		del show[i]['tests_code']
		i+=1
	return jsonify({"challenges" : show})
