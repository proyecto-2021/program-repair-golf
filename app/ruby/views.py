from . import ruby
from .models import RubyChallenge
from app import db
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.datastructures import FileStorage
import json

@ruby.route('/ruby-challenges', methods=['POST'])
def create_ruby_challenge():

    #load the ruby ​​challenge
    aux_challenge = json.loads(request.form.get('challenge'))
    aux_dict = aux_challenge['challenge']

    code_file = request.files['source_code_file']
    path_code_file = 'public/challenges/' + aux_dict['source_code_file_name'] + '.rb'
    code_file.save(dst=path_code_file)

    test_suite_file = request.files['test_suite_file']
    path_test_code_file = 'public/challenges/' + aux_dict['test_suite_file_name'] + '.rb'
    test_suite_file.save(dst=path_test_code_file)



    new_challenge = RubyChallenge(
        code = path_code_file,
        tests_code = path_test_code_file,
        repair_objective = aux_dict['repair_objective'],
        complexity = aux_dict['complexity'],
        best_score = 0
    )
    create_challenge(new_challenge)
    return jsonify({'challenge': new_challenge.get_dict()})

#verify existence in the database and add the challenge
'''
        existence_of_code = RubyChallenge.query.filter_by(code_name = aux_dict['source_code_file_name']).first()
        existence_of_test = RubyChallenge.query.filter_by(test_suite_name = aux_dict['test_suite_file_name']).first()
        if existence_of_code is None and existence_of_test is None:
'''
#output
#return make_response(jsonify({'challenge': 'the source-code and/or the test-suite have already been created'}),409)


@ruby.route('/challenge/<int:id>/repair', methods=['POST'])
def post_repair(id):
    if not exists(id):
        return make_response(jsonify({'challenge': 'NOT FOUND'}),404)

    file = request.files['source_code_file']

    file.save(dst='public/challenges/median2.rb')

    new_challenge = RubyChallenge(
        code='code',
        tests_code='tests_code',
        repair_objective='repair_objective',
        complexity='complexity',
        best_score='best_score'
    )
    #check if the posted code has not sintax errors
    challenge = get_challenge(id)
    if challenge is not None:
        test_suite = challenge.tests_code
    #run the posted code with the test suite
    #compute the score
    #if the score < challenge.score()
    #update score
    #return
    return new_challenge.get_dict()

@ruby.route('/challenge/<int:id>', methods=['GET'])
def get_ruby_challenge(id):
    if not exists(id):
        return make_response(jsonify({'challenge': 'NOT FOUND'}),404)
    challenge = get_challenge(id).get_dict()
    del challenge['id']
    return jsonify({'challenge': challenge})

@ruby.route('/challenges', methods=['GET'])
def get_all_ruby_challenges():
    challenges = get_all_challenges_dict()
    for c in challenges:
        del c['tests_code']
    return jsonify({'challenges': challenges})

def get_challenge(id):
    return db.session.query(RubyChallenge).filter_by(id=id).first()

def get_challenges():
    return db.session.query(RubyChallenge).all()

def get_all_challenges_dict():
    return list(map(lambda x: x.get_dict(), get_challenges()))

def exists(id):
    return get_challenge(id) is not None


def create_challenge(challenge):
    db.session.add(challenge)
    db.session.commit()
