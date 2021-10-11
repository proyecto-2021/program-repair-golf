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

@ruby.route('/challenge/<int:id>/repair', methods=['POST'])
def post_repair(id):
    new_challenge = RubyChallenge(
        code='code',
        tests_code='tests_code',
        repair_objetive='repair_objetive',
        complexity='complexity',
        best_score='best_score'
    )
    #check if the posted code has not sintax errors
    #challenge = get_by_id(id)
    #challege.get_test_suite()
    #run the posted code with the test suite
    #compute the score
    #if the score < challenge.score()
    #update score
    #return
    return new_challenge.get_dict()
