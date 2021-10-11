from . import ruby
from .models import RubyChallenge
from app import db
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import json

@ruby.route('/ruby-challenges', methods=['POST'])
def create_ruby_challenge():

	aux_challenge = json.loads(request.form.get('challenge'))
	aux_dict = aux_challenge['challenge']
	new_challenge = RubyChallenge(
		code = request.form.get('source_code_file'),
		tests_code = request.form.get('test_suite_file'),
		repair_objective = aux_dict['repair_objective'],
		complexity = aux_dict['complexity'],
		best_score = 0
	)

	return jsonify({'challenge': new_challenge.get_dict()})