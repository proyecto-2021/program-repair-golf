class RubyChallengeDAO(object):
	"""docstring for RubyChallengeDAO"""
	def __init__(self, arg):
		super(RubyChallengeDAO, self).__init__()
		self.arg = arg
	
	def get_challenge(id):
    return db.session.query(RubyChallenge).filter_by(id=id).first().get_dict()

	def get_challenges():
    	return [challenge.get_dict() for challenge in db.session.query(RubyChallenge).all()]

	def create_challenge(code, tests_code, repair_objective, complexity):
    	challenge = RubyChallenge(
    	    code = code,
    	    tests_code = tests_code,
    	    repair_objective = repair_objective,
    	    complexity = complexity,
    	    best_score = 0
    	)
    	db.session.add(challenge)
    	db.session.commit()
    	return challenge.get_dict()

	def update_challenge(id, changes):
 	   if len(changes) == 0:
 	       return 1
 	   result = db.session.query(RubyChallenge).filter_by(id=id).update(changes)
 	   db.session.commit()
 	   return result

	def exists(id):
 	   return get_challenge(id) is not None
