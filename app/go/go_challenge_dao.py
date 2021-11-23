from app import db
from .models_go import GoChallenge, go_attemps
from app.auth.userdao import get_user_by_id
import math
class ChallengeDAO():
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


	def exists(self, id):
		return self.get_challenge_by_id(id) is not None

	def get_attempts(self, challenge_id, user_id):
		return db.session.query(go_attemps).filter_by(challenge_id=challenge_id, user_id=user_id).first()

	def get_attempts_number(self, challenge_id, user_id):
		return self.get_attempts(challenge_id, user_id).attempts

	def add_attempt(self, challenge_id, user_id):
		go_attempts = self.get_attempts(challenge_id, user_id)
		if not go_attempts:
			challenge = db.session.query(GoChallenge).filter_by(id=challenge_id).first()
			user = get_user_by_id(user_id)
			challenge.attempts.append(user)
			db.session.commit()
		attempts = self.get_attempts_number(challenge_id, user_id)
		db.session.query(go_attemps).filter_by(challenge_id=challenge_id, user_id=user_id).update({'attempts': attempts+1})
		db.session.commit()