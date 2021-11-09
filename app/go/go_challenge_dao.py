from app import db
from . import go
from .models_go import GoChallenge

class goChallengeDAO():
	def get_all_challenges(self):
		return db.session.query(GoChallenge).all()

	def get_challenge_by_id(self, id):
		return GoChallenge.query.filter_by(id=id).first()

	def create_challenge(self, code, tests_code, repair_objective, complexity, best_score):
		new_challenge = GoChallenge(
			code = code,
			tests_code = tests_code,
			repair_objective = repair_objective,
			complexity = complexity,
			best_score = 0
			)

		db.session.add(new_challenge)
		db.session.commit()

		return new_challenge.id

	def update_challenge(self, id, challenge):
		db.session.query(GoChallenge).filter_by(id=id).update(challenge)
		db.session.commit()
