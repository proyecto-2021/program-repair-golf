from .rubychallengemodel import RubyChallengeModel, ruby_attempts
from app.auth.userdao import get_user_by_id
from app import db

class RubyChallengeDAO(object):
    def __init__(self):
        pass

    def get_challenge(self, id):
        challenge = db.session.query(RubyChallengeModel).filter_by(id=id).first().get_dict()
        del challenge['id']
        return challenge

    def get_challenges(self):
        return [challenge.get_dict() for challenge in db.session.query(RubyChallengeModel).all()]

    def create_challenge(self, code, tests_code, repair_objective, complexity):
        challenge = RubyChallengeModel(
            code = code,
            tests_code = tests_code,
            repair_objective = repair_objective,
            complexity = complexity,
            best_score = 0
        )
        db.session.add(challenge)
        db.session.commit()
        return challenge.get_dict()['id']

    def update_challenge(self, id, changes):
        db.session.query(RubyChallengeModel).filter_by(id=id).update(changes)
        db.session.commit()

    def exists(self, id):
        return db.session.query(RubyChallengeModel).filter_by(id=id).first() is not None

    def add_attempt(self, challenge_id, user_id):
        challenge_attempts = self.get_attempts(challenge_id, user_id)
        if challenge_attempts is None:
            challenge = db.session.query(RubyChallengeModel).filter_by(id=challenge_id).first()
            user = get_user_by_id(user_id)
            challenge.users_attempts.append(user) 
            db.session.commit()
        attempts = self.get_attempts_count(challenge_id, user_id)
        db.session.query(ruby_attempts).filter_by(challenge_id=challenge_id, user_id=user_id) \
            .update({'count': attempts+1})
        db.session.commit()

    def get_attempts(self, challenge_id, user_id):
        return db.session.query(ruby_attempts).filter_by(challenge_id=challenge_id, user_id=user_id).first()

    def get_attempts_count(self, challenge_id, user_id):
        return self.get_attempts(challenge_id, user_id).count