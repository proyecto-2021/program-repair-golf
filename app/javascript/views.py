from . import javascript
from .models_js import JavascriptChallenge
from flask import jsonify, make_response
from .. import db
import json
import os.path
import os

path_public = 'public/challenges/'

@javascript.route('/login')
def login():
    return { 'result': 'javascript' }

@javascript.route('javascript-challenges/<int:id>')
def update_challenge(id):

    challenge_json = loads(request.form.get('challenge')['challenge'])

    challenge = find_challenge(id)
    
    if not challenge_json: return make_response(jsonify({"challenge":"Not found: challenge request is null" }), 404)   
    if not challenge: 
        return make_response(jsonify({"challenge":"Not found: challenge no exits"}), 404) 
    
    source_code_file = request.form.get('source_code_file')
    test_suite_file = request.form.get('test_suite_file')
    repair_objetive = challenge_json['repair_objective']
    complexity = challenge_json['complexity']

    if source_code_file:
        challenge.code = os.path.basename(source_code_file)
        #Todo: Subir archivo source_code_file 
    if test_suite_file:
        challenge.tests_code = os.path.basename(test_suite_file)
        #Todo: Subir archivo test_suite_file
    if repair_objetive:
        challenge.repair_objetive = repair_objetive
    if complexity:
        challenge.complexity = complexity

    db.session.commit()
    return make_response(jsonify({"challenge": [challenge]}), 200)
    
def find_challenge(id_challenge):
    return JavascriptChallenge.query.filter_by(id=id_challenge).first()    