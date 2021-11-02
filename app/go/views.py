import os
from . import go
from .models_go import GoChallenge
from app import db
from flask import jsonify, make_response


@go.route('/api/v1/go-challenges', methods=['GET'])
def get_all_challenges():
    challenges = db.session.query(GoChallenge).all()
    if not challenges:
        return make_response(jsonify({'challenges' : 'not found'}), 400)
    
    challenges_to_show = []
    i = 0
    
    for challenge in challenges:
        challenge_dict = challenge.convert_dict()
        from_file_to_str(challenge_dict)
        challenges_to_show.append(challenge_dict)
        del challenges_to_show[i]['tests_code']
        i+=1

    return jsonify({"challenges" : challenges_to_show})


@go.route('/api/v1/go-challenges/<id>', methods=['GET'])
def return_single_challenge(id):
        challenge_by_id=GoChallenge.query.filter_by(id=id).first()
        if challenge_by_id is None:
            return "ID Not Found", 404
        challenge_to_return=challenge_by_id.convert_dict()
        from_file_to_str(challenge_to_return)
        from_file_to_str_tests(challenge_to_return)
        del challenge_to_return["id"]
        return jsonify({"challenge":challenge_to_return})


def from_file_to_str(challenge):
    file= open(str(os.path.abspath(challenge["code"])),'r')
    content=file.readlines()
    file.close()
    challenge["code"]=content
    return challenge

def from_file_to_str_tests(challenge):
    file= open(str(os.path.abspath(challenge["tests_code"])),'r')
    content=file.readlines()
    file.close()
    challenge["tests_code"]=content
    return challenge