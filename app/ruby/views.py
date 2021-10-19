from . import ruby
from .models import RubyChallenge
from app import db
from flask import jsonify, request, make_response
from shutil import copy
import subprocess, json, os, sys
import nltk

@ruby.route('/challenge', methods=['POST'])
def create_ruby_challenge():

    input_challenge = json.loads(request.form.get('challenge'))
    dictionary = input_challenge['challenge']

    file = request.files['source_code_file']
    file_path = 'public/challenges/' + dictionary['source_code_file_name'] + '.rb'

    test_file = request.files['test_suite_file']
    test_file_path = 'public/challenges/' + dictionary['test_suite_file_name'] + '.rb'

    #check that the same files is not posted again
    if not save(file, file_path):
        return make_response(jsonify({'challenge': 'source_code is already exist'}),409)
    
    if not save(test_file, test_file_path):
        return make_response(jsonify({'challenge': 'test_suite is already exist'}),409)

    #check no syntaxis errors
    if not (compiles(file_path) and compiles(test_file_path)):
        os.remove(file_path)
        os.remove(test_file_path)
        return make_response(jsonify({'challenge': 'source_code and/or test_suite not compile'}),400)

    if  not dependencies_ok(test_file_path, dictionary['source_code_file_name']):
        os.remove(file_path)
        os.remove(test_file_path)
        return make_response(jsonify({'challenge': 'test_suite dependencies are wrong'}),400)

    new_challenge = RubyChallenge(
        code = file_path,
        tests_code = test_file_path,
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
    file_name = 'public/' + os.path.basename(challenge['code'])
    file.save(dst=file_name)

    if not compiles(file_name):
        os.remove(file_name)
        return make_response(jsonify({'challenge': {'repair_code': 'is erroneous'}}),400)

    test_file_name = 'public/tmp.rb'
    copy(challenge['tests_code'], test_file_name)

    if tests_fail(test_file_name):
        os.remove(file_name)
        os.remove(test_file_name)
        return make_response(jsonify({'challenge': {'tests_code': 'fails'}}),200)

    with open(challenge['code']) as f1, open(file_name) as f2:
        score = nltk.edit_distance(f1.read(),f2.read())

    if (score < challenge['best_score']) or (challenge['best_score'] == 0):
        update_challenge(id, {'best_score': score})

    os.remove(file_name)
    os.remove(test_file_name)

    challenge = get_challenge(id).get_dict()
    delete_keys(challenge, ['id','code','complexity','tests_code'])
    return jsonify( {'repair' :
                        {
                            'challenge': challenge,
                            'player': {'username': 'Agustin'},
                            'attemps': '1',
                            'score': score
                        }
                    }
                )

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
    source_code_path_tmp = f"public/{source_code_name}"
    source_test_name = f"{update_data['test_suite_file_name']}.rb"
    source_test_path_tmp = f"public/{source_test_name}"
    delete_keys(update_data, ['source_code_file_name', 'test_suite_file_name'])

    if 'source_code_file' in request.files:
        request.files['source_code_file'].save(dst=source_code_path_tmp)
        if os.path.isfile(source_code_path_tmp) and not compiles(source_code_path_tmp):
            os.remove(source_code_path_tmp)
            return make_response(jsonify({'code': "doesn't compile or doesn't exists"}), 400)
    else:
        update_file_name(old_challenge, 'code', source_code_name, update_data)

    if 'test_suite_file' in request.files:
        request.files['test_suite_file'].save(dst=source_test_path_tmp)
        if os.path.isfile(source_test_path_tmp) and not tests_fail(source_test_path_tmp):
            os.remove(source_test_path_tmp)
            return make_response(jsonify({'tests': "tests must fail or doesn't exists"}), 400)
        if not dependencies_ok(source_test_path_tmp, os.path.basename(source_code_name.split('.')[0])):
            os.remove(source_test_path_tmp)
            return make_response(jsonify({'tests': "dependencies failed to compile"}), 400)
    else:
        if not dependencies_ok(old_challenge['tests_code'], os.path.basename(source_code_name.split('.')[0])):
            return make_response(jsonify({'tests': "dependencies failed to compile"}), 400)
        update_file_name(old_challenge, 'tests_code', source_test_name, update_data)
        
    if update_challenge(id, update_data) < 1:
        return make_response(jsonify({'challenge': "update failed check input data"}), 400)

    update_file(old_challenge, 'code', source_code_path_tmp, source_code_name, update_data)
    update_file(old_challenge, 'tests_code', source_test_path_tmp, source_test_name, update_data)

    update_challenge(id, update_data)
    
    updated_challenge = get_challenge(id).get_dict()
    delete_keys(updated_challenge, ['id'])
    return jsonify({'challenge': updated_challenge})

def delete_keys(dictionary, key_list):
    for key in key_list:
        del dictionary[key]

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

def save(file, path):
    if os.path.isfile(path):
        return False
    file.save(dst=path)
    return True

def file_exists(f):
    return os.path.isfile(f)

def update_file(challenge, file_type, source_path, source_name, data):
    if file_exists(source_path):
        os.remove(challenge[file_type])
        data[file_type] = copy(source_path, f"public/challenges/{source_name}")
        os.remove(source_path)

def update_file_name(challenge, file_type, source_name, data):
    if (os.path.basename(challenge[file_type]) != source_name):
        new_name = f"public/challenges/{source_name}"
        os.rename(challenge[file_type], new_name)
        data[file_type] = new_name

def compiles(file_name):
    command = 'ruby -c ' + file_name
    return (subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0)

def tests_fail(test_file_name):
    command = 'ruby ' + test_file_name
    return (subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) != 0)

def dependencies_ok(test_file_path, file_name):
    command = 'grep "require_relative" ' + test_file_path
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    dependence_name = (p.communicate()[0].decode(sys.stdout.encoding).strip().split("'")[1])
    return dependence_name == file_name