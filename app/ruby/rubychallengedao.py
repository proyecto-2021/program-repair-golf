from .models import RubyChallenge
from app import db

class RubyChallengeDAO(object):
	def __init__(self):
		pass

	def get_challenge(self, id):
		return db.session.query(RubyChallenge).filter_by(id=id).first().get_dict()

	def get_challenge_data(self, id):
		challenge = db.session.query(RubyChallenge).filter_by(id=id).first().get_data()
		del challenge['id']
		return challenge

	def get_challenges(self):
		return [challenge.get_dict() for challenge in db.session.query(RubyChallenge).all()]

	def get_challenges_data(self):
		challenges = [challenge.get_data() for challenge in db.session.query(RubyChallenge).all()]
		for c in challenges:
			del c['tests_code']
		return challenges

	def create_challenge(self, code, tests_code, repair_objective, complexity):
		challenge = RubyChallenge(
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
		if len(changes) == 0:
			return 1
		result = db.session.query(RubyChallenge).filter_by(id=id).update(changes)
		db.session.commit()
		return result

	def exists(self, id):
		return get_challenge(id) is not None