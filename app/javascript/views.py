from . import javascript
from flask import jsonify, make_response
from .models import JavaScriptChallenges

@javascript.route('/login')
def login():
    return { 'result': 'javascript' }

@javascript.rout('/api/v1/javascript-challenges', methods=['GET'])
def javascipt_challenges():
    challenges = JavaScriptChallenges.query(id,code,repair_objective,complexity).all()
    return make_response(jsonify({"challenges" : [challenges]}), 200)