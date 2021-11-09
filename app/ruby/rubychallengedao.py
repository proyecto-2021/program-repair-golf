from .rubychallengemodel import RubyChallengeModel
from app import db

class RubyChallengeDAO(object):
	def __init__(self):
		pass

	def get_challenge(self, id):
		challenge = db.session.query(RubyChallengeModel).filter_by(id=id).first().get_dict()
		del challenge['id']
		return challenge

	def get_challenges(self):
		return db.session.query(RubyChallengeModel).all()

	def get_challenge_data(self, id):
		challenge = db.session.query(RubyChallengeModel).filter_by(id=id).first().get_data()
		del challenge['id']
		return challenge

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
		result = db.session.query(RubyChallengeModel).filter_by(id=id).update(changes)
		db.session.commit()

	def exists(self, id):
		return db.session.query(RubyChallengeModel).filter_by(id=id).first() is not None