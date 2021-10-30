from .. import db
class JavascriptChallenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(256))
    tests_code = db.Column(db.String(256))
    repair_objective = db.Column(db.String(128))
    complexity = db.Column(db.Integer)
    best_score =  db.Column(db.Integer)

    def to_dict(self):
        return{
            "id": self.id,
            "code": self.code,
            "tests_code": self.tests_code,
            "repair_objective": self.repair_objective,
            "complexity": self.complexity,
            "best_score": self.best_score
        }

    def find_challenge(id_challenge):
        return JavascriptChallenge.query.filter_by(id=id_challenge).first()