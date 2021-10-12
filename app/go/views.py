from . import go
from models_go import GoChallenge
from flask import request, jsonify
from .. import db

@go.route('/hello') 
def hello():
    return 'Hello World!'

@go.route('/api/v1/go-challenges/<id>', methods=['GET'])
    def return_single_challenge(id):
        challenge_by_id=GoChallenge.query.filter_by(name=id).first()
        if challenge_by_id is None:
            return "ID Not Found", 404
        #code=open(str(challenge_by_id.code),'r')
        #code_for_dict=""
        #for linea in code:
        #    code_for_dict + linea +"\n"
        challenge_to_return={
        #    "code":code_for_dict,
            "code":challenge_by_id.code,
            "tests_code":challenge_by_id.tests_code,
            "repair_objective":challenge_by_id.repair_objective,
            "complexity":challenge_by_id.complexity,
            "score":challenge_by_id.score,
        }
        return jsonify({"challenge":challenge_to_return})