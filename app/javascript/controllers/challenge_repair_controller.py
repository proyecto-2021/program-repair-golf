import nltk
from flask import make_response,jsonify
from files_controller import open_file, exist_file, to_temp_file
from .. import db

def repair():
    return True

def repair_ok():   
    return True

def update_score(challenge,score):
    challenge.best_score = score
    db.session.commit()
    return challenge

def calculate_score(challenge):
    file_path_new = to_temp_file(challenge.code) 
    return nltk.edit_distance(open_file(challenge.code), open_file(file_path_new))