from flask import jsonify, make_response
from .models_js import JavascriptChallenge


def list_challenges_js():
    challenges = {"challenge":[]}
    challenges["challenge"] = JavascriptChallenge.query.all()
    challenge_all = []
    
    for x in challenges['challenge']:
        challenge_all.append(x.to_dict())
    return make_response(jsonify({"challenges":challenge_all}))
