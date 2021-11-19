from app import db

java_attempts = db.Table('java_attempts',
    db.Column('challenge_id', db.Integer, db.ForeignKey('challenge_java.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('attempts', db.Integer, default=0)
)

class Challenge_java(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128), nullable=False)
    tests_code = db.Column(db.String(128),nullable=False)
    repair_objective = db.Column(db.String(128),nullable=False)
    complexity = db.Column(db.Integer,nullable=False)
    score = db.Column(db.Integer)
    attempts_by_users = db.relationship('User', secondary=java_attempts)

    def __repr__(self):
        challenge = {
            "id": self.id,
            "code": self.code,
            "tests_code": self.tests_code,
            "repair_objective": self.repair_objective,
            "complexity": self.complexity,
            "best_score": self.score
        }
        return challenge