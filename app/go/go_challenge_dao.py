from app import db
from . import go
from .models_go import GoChallenge

class goChallengeDAO():
	def get_all_challenges():
		return db.session.query(GoChallenge).all()

	def get_challenge_by_id(id):
		return GoChallenge.query.filter_by(id=id).first()

	def create_challenge(challenge):
		new_challenge = GoChallenge(
			code = challenge.code,
			tests_code = challenge.tests_code,
			repair_objective = challenge.repair_objective,
			complexity = challenge.complexity,
			best_score = 0)

		db.session.add(new_challenge)
		db.session.commit()

		return new_challenge.id

	def update_challenge(id, challenge):
		db.session.query(GoChallenge).filter_by(id=id).update(challenge)
		db.session.commit()
