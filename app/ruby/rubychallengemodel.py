from app import db

class RubyChallengeModel(db.Model):
	__tablename__ = 'RubyChallenge'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(256))  # Path to source file
	tests_code = db.Column(db.String(256))  # Path to test suite file
	repair_objective = db.Column(db.String(128))
	complexity = db.Column(db.String(3))
	best_score = db.Column(db.Integer())

	def get_dict(self):
		return {
			"id": self.id,
			"code": self.code,
			"tests_code": self.tests_code,
			"repair_objective": self.repair_objective,
			"complexity": self.complexity,
			"best_score": self.best_score
		}