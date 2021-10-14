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
	for i in challenges:
		show.append(GoChallenge.convert_dict(i))
	return jsonify({"challenges" : show})

'''
@app.route('api/v1/go-challenges/<int:id>', methods=['PUT'])
def update_challenge(id):
'''
