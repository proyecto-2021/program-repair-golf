from app import db

class CSharpChallengeModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(256), unique=True, nullable=False)
    tests_code = db.Column(db.String(256), nullable=False)
    repair_objective = db.Column(db.String(120), nullable=False)
    complexity = db.Column(db.Integer, nullable=False)
    best_score = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return {
            "id": self.id,
            "code": self.code,
            "tests_code": self.tests_code,
            "repair_objective": self.repair_objective,
            "complexity": self.complexity,
            "best_score": self.best_score
        }
    
