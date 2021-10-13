from . import python
from .. import db
from flask import request, make_response, jsonify
from .models import PythonChallenge
from json import loads

@python.route('/login', methods=['GET'])
def login():
    return { 'result': 'ok' }

@python.route('/api/v1/python-challenges', methods=['GET'])
def return_challenges(): 
    all_challenges = PythonChallenge.query.all()
    challenge_list = []
    for challenge in all_challenges:
        aux_dict = PythonChallenge.to_dict(challenge)
        aux_dict.pop('tests_code', None)
        challenge_list.append(aux_dict)
    return jsonify({"challenges": challenge_list})

@python.route('/api/v1/python-challenges/<id>', methods=['GET'])
def return_challange_id(id):
    challenge = PythonChallenge.query.filter_by(id = id).first()
    if challenge is None:
        return make_response(jsonify({"Challenge": "Not found"}), 404)
    aux_dict = PythonChallenge.to_dict(challenge)
    aux_dict.pop('id', None)
    return jsonify({"Challenge": aux_dict}) 

@python.route('/api/v1/python-challenges', methods=['POST'])
def create_new_challenge():
    challenge_data = loads(request.form.get('challenge'))['challenge']
    
    path_to_code = request.form.get('source_code_file')
    path_to_tests = request.form.get('test_suite_file')

    #if the challenge is invalid, an error will be returned
    #valid_python_challenge(challenge_data, path_to_code, path_to_tests)
        
    new_challenge = PythonChallenge(code=path_to_code,
        tests_code=path_to_tests,
        repair_objective=challenge_data['repair_objective'],
        complexity=challenge_data['complexity'],
        best_score=0)

    db.session.add(new_challenge)
    db.session.commit()

    req_challenge = PythonChallenge.query.filter_by(id=new_challenge.id).first()
    return jsonify({"challenge" : PythonChallenge.to_dict(req_challenge)})


@python.route('api/v1/python-challenges/<id>', methods=['PUT'])
def update_challenge(id):
    challenge_data = loads(request.form.get('challenge'))['challenge']

    req_challenge = PythonChallenge.query.filter_by(id=id).first()

    if req_challenge is None:
        return make_response(jsonify({"challenge":"there is no challenge with that id"}),404)
    else:
        db.session.query(PythonChallenge).filter_by(id=id).update(dict( complexity = challenge_data['complexity']))
        db.session.commit()
        req_challenge = PythonChallenge.query.filter_by(id=id).first()
        dictionary =  PythonChallenge.to_dict(req_challenge)
        dictionary.pop('id', None)
        return jsonify({"challenge" : dictionary})

