from app.cSharp.models import CSharpChallengeModel
from app import db
import os


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
        new_challenge = CSharpChallengeModel(code=source_code_path,
                                             tests_code=test_path,
                                             repair_objective=challenge_data['repair_objective'],
                                             complexity=int(challenge_data['complexity']),
                                             best_score=0)
        db.session.add(new_challenge)
        db.session.commit()
        return new_challenge.id

    def update_challenge_data(self, id, data):
        db.session.query(CSharpChallengeModel).filter_by(id=id).update(data)
        db.session.commit()

    def save_best_score(self, score, previous_best_score, chall_id):
        if previous_best_score == 0 or previous_best_score > score:
            challenge = db.session.query(CSharpChallengeModel).filter_by(id=chall_id)
            challenge.update(dict(best_score=score))
            db.session.commit()
            return 0
        else:
            return 1

    def remove(self, *paths):
        for path in paths:
            os.remove(path)
