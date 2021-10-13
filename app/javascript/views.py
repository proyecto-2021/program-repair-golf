from . import javascript
from .models_js import JavaScriptChallenge
from flask import Flask, jsonify, request
from .. import db
import json

@javascript.route('/login')
def login():
    return { 'result': 'javascript' }


@javascript.route('/javascript-challenges', methods=['POST'])
def createChallengeJS():
  #challenge_json = request.get_json() if request.get_json() else None
  
  challenge_json = json.loads(request.form.get('challenge'))

  newChallengeJS = JavaScriptChallenge(code = request.form.get('source_code_file'),
                                      tests_code = request.form.get('test_suite_file'),
                                      repair_objective = challenge_json['challenge']['repair_objective'],
                                      complexity = challenge_json['challenge']['complexity'],
                                      best_score = 0)
    
  db.session.add(newChallengeJS)
  db.session.commit()
  
  return jsonify({'challenge': newChallengeJS.get_dict()})