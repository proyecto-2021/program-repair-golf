import nltk
from flask import make_response,jsonify,request
from controllers.files_controller import open_file, exist_file, to_temp_file, replace_file,upload_file
from .. import db
from ..modules.source_code_module import compile_js, test_run

def repair(challenge):
    challenge_dict = challenge.to_dict()

    for k in ['id','code','complexity','tests_code']:
        del challenge_dict[k]

    return make_response(jsonify( {'repair' :{
                    'challenge': challenge_dict,
                    'player': {'username': 'user'},
                    'attemps': '1',
                    'score': calculate_score
                    }}, 200))


def update_score(challenge,score):
    challenge.best_score = score
    db.session.commit()
    return challenge

def calculate_score(challenge):
    file_path_new = to_temp_file(challenge.code) 
    return nltk.edit_distance(open_file(challenge.code), open_file(file_path_new))