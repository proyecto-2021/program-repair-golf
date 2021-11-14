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

    def save_challenge(self, challenge_data, source_code_path, test_path):
        new_challenge = CSharpChallengeModel(code = source_code_path, tests_code = test_path, repair_objective = challenge_data['repair_objective'], complexity = int(challenge_data['complexity']), best_score = 0)
        db.session.add(new_challenge)
        db.session.commit()
        return new_challenge.id

    def update_challenge_data(self, id, data):
        db.session.query(CSharpChallengeModel).filter_by(id=id).update(data)
        db.session.commit()
