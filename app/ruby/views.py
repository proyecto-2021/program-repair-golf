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

    test_file_name = 'public/repair_executions/tmp_test.rb'
    copy(challenge['tests_code'], test_file_name)

    if tests_fail(test_file_name):
        return make_response(jsonify({'challenge': {'tests_code': 'fails'}}),200)

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

@ruby.route('/challenge/<int:id>', methods=['PUT'])
def update_ruby_challenge(id):
    if not exists(id):
        return make_response(jsonify({'challenge': 'NOT FOUND'}), 404)
    update_data = json.loads(request.form.get('challenge'))['challenge']
    old_challenge = get_challenge(id).get_dict()
    source_code_name = f"{update_data['source_code_file_name']}.rb"
    source_test_name = f"{update_data['test_suite_file_name']}.rb"
    del update_data['source_code_file_name']
    del update_data['test_suite_file_name']

    if 'source_code_file' in request.files:
        source_code_file = request.files['source_code_file']
        source_code_path_tmp = f"public/{source_code_name}"
        source_code_file.save(dst=source_code_path_tmp)
        if os.path.isfile(source_code_path_tmp) and not compiles(source_code_path_tmp):
            os.remove(source_code_path_tmp)
            return make_response(jsonify({'code': "doesn't compile"}), 400)

    if 'test_suite_file' in request.files:
        source_test_file = request.files['test_suite_file']
        source_test_path_tmp = f"public/{source_test_name}"
        source_test_file.save(dst=source_test_path_tmp)
        if os.path.isfile(source_test_path_tmp) and not tests_fail(source_test_path_tmp):
            os.remove(source_test_path_tmp)
            return make_response(jsonify({'tests': "tests must fail"}), 400)
        
    if update_challenge(id, update_data) < 1:
        return make_response(jsonify({'challenge': "update failed check input data"}), 400)

    update_file(old_challenge, 'code', source_code_path_tmp, source_code_name, update_data)
    update_file(old_challenge, 'tests_code', source_test_path_tmp, source_test_name, update_data)
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
    result = db.session.query(RubyChallenge).filter_by(id=id).update(changes)
    db.session.commit()
    return result

def save(key, file_name):
    file = request.files[key]
    path = 'public/challenges/' + file_name + '.rb'
    file.save(dst=path)
    return path

def file_exists(f):
    return os.path.isfile(f)

def update_file(challenge, file_type, source_path, source_name, data):
    if file_exists(source_path):
        os.remove(challenge[file_type])
        data[file_type] = copy(source_path, f"public/challenges/{source_name}")
        os.remove(source_path)
    elif (os.path.basename(challenge[file_type]) != source_name):
        new_path = f"public/challenges/{source_name}"
        os.rename(challenge[file_type], new_path)
        data[file_type] = new_path

def compiles(file_name):
    command = 'ruby -c ' + file_name
    return (subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0)

def tests_fail(test_file_name):
    command = 'ruby ' + test_file_name
    return (subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) != 0)