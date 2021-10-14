from . import ruby
from .models import RubyChallenge
from app import db
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.datastructures import FileStorage
from shutil import copy
import subprocess
import json
import os

@ruby.route('/challenge', methods=['POST'])
def create_ruby_challenge():

    input_challenge = json.loads(request.form.get('challenge'))
    dictionary = input_challenge['challenge']

    code_path = save('source_code_file', dictionary['source_code_file_name'])
    test_code_path = save('test_suite_file', dictionary['test_suite_file_name'])

    new_challenge = RubyChallenge(
        code = code_path,
        tests_code = test_code_path,
        repair_objective = dictionary['repair_objective'],
        complexity = dictionary['complexity'],
        best_score = 0
    )

    create_challenge(new_challenge)
    return jsonify({'challenge': new_challenge.get_dict()})

@ruby.route('/challenge/<int:id>/repair', methods=['POST'])
def post_repair(id):
    if not exists(id):
        return make_response(jsonify({'challenge': 'NOT FOUND'}),404)

    challenge = get_challenge(id).get_dict()
    
    file = request.files['source_code_file']
    #The file must be saved with the same name has the original code, else the test suite will not work
    #file_name = 'public/challenges/' + + '.rb'
    file_name = 'public/repair_executions/' + os.path.basename(challenge['code'])
    file.save(dst=file_name)

    if not compiles(file_name):
        return make_response(jsonify({'challenge': {'repair_code': 'is erroneous'}}),400)

    copy(challenge['tests_code'],'public/repair_executions/tmp_test.rb')

    #run the posted code with the test suite
    #compute the score
    #if the score < challenge.score()
    #update score
    #return
    return challenge

@ruby.route('/challenge/<int:id>', methods=['GET'])
def get_ruby_challenge(id):
    if not exists(id):
        return make_response(jsonify({'challenge': 'NOT FOUND'}),404)

    challenge = get_challenge(id).get_dict()
    del challenge['id']

    code_path = challenge['code']
    tests_code_path = challenge['tests_code']

    with open(code_path) as f:
        challenge['code'] = f.read()

    with open(tests_code_path) as f:
        challenge['tests_code'] = f.read()

    return jsonify({'challenge': challenge})

@ruby.route('/challenges', methods=['GET'])
def get_all_ruby_challenges():
    challenges = get_all_challenges_dict()
    
    for c in challenges:
        del c['tests_code']
        code_path = c['code']
        with open(code_path) as f:
            c['code'] = f.read()

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

def save(key, file_name):
    file = request.files[key]
    path = 'public/challenges/' + file_name + '.rb'
    file.save(dst=path)
    return path

def compiles(file_name):
    command = 'ruby -c ' + file_name
    return (subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0)
