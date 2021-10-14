from . import ruby
from .models import RubyChallenge
from app import db
from flask import Flask, jsonify, request, make_response
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from werkzeug.datastructures import FileStorage
import json
import os.path
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

@ruby.route('/challenge/<int:id>', methods=['PUT'])
def update_ruby_challenge(id):
    if not exists(id):
        return make_response(jsonify({'challenge': 'NOT FOUND'}), 404)
    update_data = json.loads(request.form.get('challenge'))['challenge']
    objective_challenge = get_challenge(id).get_dict()
    
    update_file(objective_challenge, 'code', update_data)
    update_file(objective_challenge, 'tests_code', update_data)
    
    # Default value needed for this parameters. It must take the current file name.
    del update_data['source_code_file_name'] # This keys are no longer needed for updating the challenge.
    del update_data['test_suite_file_name']

    update_challenge(id, update_data)
    updated_challenge = get_challenge(id).get_dict()
    del updated_challenge['id']
    return jsonify({'challenge': updated_challenge})

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

def update_challenge(id, changes):
    db.session.query(RubyChallenge).filter_by(id=id).update(changes)
    db.session.commit()

def save(key, file_name):
    file = request.files[key]
    path = 'public/challenges/' + file_name + '.rb'
    file.save(dst=path)
    return path

def file_exists(f, persistent=True):
    if not persistent:
        return (f in request.files)
    return os.path.isfile(f)

def update_file(challenge, file_type, data):
    source_file = ''
    if file_type == 'code':
        source_file = 'source_code_file'
    else:
        source_file = 'test_suite_file'
    source_file_name = f"{source_file}_name"

    if file_exists(source_file, persistent=False):
        os.remove(challenge[file_type])
        data[file_type] = save(source_file, data[source_file_name])
    elif (os.path.basename(challenge[file_type]).split('.')[0] != data[source_file_name]):
        new_path = f"public/challenges/{data[source_file_name]}.rb"
        os.rename(challenge[file_type], new_path)
        data[file_type] = new_path