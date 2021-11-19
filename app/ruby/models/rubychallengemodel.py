from app import db
from sqlalchemy.sql.schema import CheckConstraint

ruby_attempts = db.Table('ruby_attempts',
    db.Column('challenge_id', db.Integer, db.ForeignKey('ruby_challenge.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('count', db.Integer, default=0)
)

class RubyChallengeModel(db.Model):
	"""Model to create a table in database."""
	__tablename__ = 'ruby_challenge'
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String(256))  # Path to source file
	tests_code = db.Column(db.String(256))  # Path to test suite file
	repair_objective = db.Column(db.String(128))
	complexity = db.Column(db.String(1, CheckConstraint("complexity IN ('1', '2', '3', '4', '5')")))
	best_score = db.Column(db.Integer)
	users_attempts = db.relationship('User', secondary=ruby_attempts)

	def get_dict(self):
		"""Convert RubyChallengeModel into dict."""
		return {
			"id": self.id,
			"code": self.code,
			"tests_code": self.tests_code,
			"repair_objective": self.repair_objective,
			"complexity": self.complexity,
			"best_score": self.best_score
		}