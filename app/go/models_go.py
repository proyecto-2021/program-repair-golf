from app import db
#from ..auth.usermodel import User

go_attemps = db.Table('go_attemps',
    db.Column("challenge_id", db.Integer, db.ForeignKey("go_challenge.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("attempts",db.Integer,default=0)
)

class GoChallenge(db.Model):
    __tablename__ = "go_challenge"
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(256)) 
    tests_code = db.Column(db.String(256))
    repair_objective = db.Column(db.String(128))
    complexity = db.Column(db.String(3))
    best_score = db.Column(db.Integer())
    attempts = db.relationship('User', secondary=go_attemps)

    def convert_dict(self):
        return {"id": self.id,
                "code": self.code,
                "tests_code": self.tests_code,
                "repair_objective": self.repair_objective,
                "complexity": self.complexity,
                "best_score": self.best_score}