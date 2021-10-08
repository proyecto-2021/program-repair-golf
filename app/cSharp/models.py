from app import db

class CSharp_Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(256), unique=True, nullable=False)
    tests_code = db.Column(db.String(256), nullable=False)
    repair_objetive = db.Column(db.String(120), nullable=False)
    complexity = db.Column(db.Integer, nullable=False)
    best_score = db.Column(db.Integer, nullable=False)