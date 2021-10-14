from .. import db
from dataclasses import dataclass

@dataclass
class JavascriptChallenge(db.Model):
    id: int
    code: str
    tests_code: str 
    repair_objective: str
    complexity: int
    best_score: int

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(256))
    tests_code = db.Column(db.String(256))
    repair_objective = db.Column(db.String(128))
    complexity = db.Column(db.Integer)
    best_score =  db.Column(db.Integer)