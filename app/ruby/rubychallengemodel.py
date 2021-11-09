from app import db
from sqlalchemy.sql.schema import CheckConstraint

class RubyChallengeModel(db.Model):
	__tablename__ = 'ruby_challenge'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(256))  # Path to source file
	tests_code = db.Column(db.String(256))  # Path to test suite file
	repair_objective = db.Column(db.String(128))
	complexity = db.Column(db.String(1, CheckConstraint("complexity IN ('1', '2', '3', '4', '5')")))
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

	def get_data(self):
		with open(self.code) as f1:
			code_content = f1.read()
		with open(self.tests_code) as f2:
			tests_code_content = f2.read()

		return {
			"id":self.id,
			"code":code_content,
			"tests_code":tests_code_content,
			"repair_objective":self.repair_objective,
			"complexity":self.complexity,
			"best_score":self.best_score
		}