from app import db

class Challenge_java(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(128), nullable=False)
    tests_code = db.Column(db.String(128),nullable=False)
    repair_objective = db.Column(db.String(128),nullable=False)
    complexity = db.Column(db.Integer,nullable=False)
    score = db.Column(db.Integer)

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