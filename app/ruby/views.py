from . import ruby
from .models import RubyChallenge
from app import db
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import json

@ruby.route('/ruby-challenges', methods=['POST'])
def create_ruby_challenge():
	#load the ruby ​​challenge
	aux_challenge = json.loads(request.form.get('challenge'))
	aux_dict = aux_challenge['challenge']
	new_challenge = RubyChallenge(
		code = request.form.get('source_code_file'),
		tests_code = request.form.get('test_suite_file'),
		#code_name = aux_dict['source_code_file_name'],
		#tests_code_name = aux_dict['test_suite_file_name'],
		repair_objective = aux_dict['repair_objective'],
		complexity = aux_dict['complexity'],
		best_score = 0
	)
	db.session.add(new_challenge)
	db.session.commit()
	return jsonify({'challenge': new_challenge.get_dict()})
'''
	#verify existence in the database and add the challenge
	existence_of_code = RubyChallenge.query.filter_by(code_name = aux_dict['source_code_file_name']).first()
	existence_of_test = RubyChallenge.query.filter_by(test_suite_name = aux_dict['test_suite_file_name']).first()
	if existence_of_code is None and existence_of_test is None:
'''
	#output
	#return make_response(jsonify({'challenge': 'the source-code and/or the test-suite have already been created'}),409)
