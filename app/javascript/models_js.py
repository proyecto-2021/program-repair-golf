from .. import db

javascript_attempts = db.Table('javascript_attempts',
    db.Column('challenge_id', db.Integer, db.ForeignKey('javascript_challenge.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('count', db.Integer, default=0)
)

class JavascriptChallenge(db.Model):
    __tablename__ = 'javascript_challenge'
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(256))
    tests_code = db.Column(db.String(256))
    repair_objective = db.Column(db.String(128))
    complexity = db.Column(db.Integer)
    best_score =  db.Column(db.Integer)
    users_attempts = db.relationship('User', secondary=javascript_attempts)
    
    def to_dict(self):
        return{
            "id": self.id,
            "code": self.code,
            "tests_code": self.tests_code,
            "repair_objective": self.repair_objective,
            "complexity": self.complexity,
            "best_score": self.best_score
        }

