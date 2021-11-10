from app import db
from . import go
from .models_go import GoChallenge

class goChallengeDAO():
	def __init__(self):
		pass 

	def get_all_challenges(self):
		return db.session.query(GoChallenge).all()

	def get_challenge_by_id(self, id):
		#return GoChallenge.query.filter_by(id=id).first()
		return db.session.query(GoChallenge).filter_by(id=id).first()

	def create_challenge(self, challenge):
		new_challenge = GoChallenge(
			code = challenge.code,
			tests_code = challenge.tests_code,
			repair_objective = challenge.repair_objective,
			complexity = challenge.complexity,
			best_score = 0
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
		return get_challenge_by_id(id) is not Nones
