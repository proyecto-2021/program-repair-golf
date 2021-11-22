from app import db

c_sharp_attempts = db.Table('c_sharp_attempts',
    db.Column('challenge_id', db.Integer, db.ForeignKey('c_sharp_challenge_model.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('attempts', db.Integer, default=0)
)


class CSharpChallengeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(256), unique=True, nullable=False)
    tests_code = db.Column(db.String(256), nullable=False)
    repair_objective = db.Column(db.String(120), nullable=False)
    complexity = db.Column(db.Integer, nullable=False)
    best_score = db.Column(db.Integer, nullable=False)
    users_attempts = db.relationship('User', secondary=c_sharp_attempts)

    def __repr__(self):
        return {
            "id": self.id,
            "code": self.code,
            "tests_code": self.tests_code,
            "repair_objective": self.repair_objective,
            "complexity": self.complexity,
            "best_score": self.best_score
        }
