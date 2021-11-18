import math
from app import db
from . import go
from .models_go import GoChallenge
class goChallengeDAO():
	def __init__(self):
		pass 

	def get_all_challenges(self):
		return db.session.query(GoChallenge).all()

	def get_challenge_by_id(self, id):
		return db.session.query(GoChallenge).filter_by(id=id).first()

	def create_challenge(self, code, tests, repair_objective, complexity):
		new_challenge = GoChallenge(
			code = code,
			tests_code = tests,
			repair_objective = repair_objective,
			complexity = complexity,
			best_score = math.inf
			)

		db.session.add(new_challenge)
		db.session.commit()

		return new_challenge.id

	def update_challenge(self, id, challenge):
		db.session.query(GoChallenge).filter_by(id=id).update(challenge)
		db.session.commit()

	def delete_challenge(self, challenge):
		db.session.delete(challenge)
		db.session.commit()

	def exists(self, id):
		return self.get_challenge_by_id(id) is not None
