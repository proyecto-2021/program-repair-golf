from app.cSharp.models import CSharpChallengeModel
from app import db

class CSharpChallengeDAO:

    def __init__(self):
        pass

    def get_challenge_db(self, id, show_files_content=False):
        challenge = db.session.query(CSharpChallengeModel).filter_by(id=id).first().__repr__()
        print(challenge)
        if show_files_content:
            challenge['code'] = open(challenge['code'], "r").read()
            challenge['tests_code'] = open(challenge['tests_code'], "r").read() 
        return challenge 
        
    def exist(self, id):
        return db.session.query(CSharpChallengeModel).filter_by(id=id).first() is not None