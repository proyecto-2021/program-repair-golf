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
    
def get_challenge_db(id, show_files_content=False):
    challenge = db.session.query(CSharp_Challenge).filter_by(id=id).first().__repr__()
    if show_files_content:
        challenge['code'] = open(challenge['code'], "r").read()
        challenge['tests_code'] = open(challenge['tests_code'], "r").read() 
    return challenge

def exist(id):
    return get_challenge_db(id) is not None

def save_challenge(challenge_data, source_code_path, test_path):
    new_challenge = CSharp_Challenge(code = source_code_path, tests_code = test_path, repair_objetive = challenge_data['repair_objective'], complexity = int(challenge_data['complexity']), best_score = 0)
    db.session.add(new_challenge)
    db.session.commit()
    return new_challenge.id

def update_challenge_data(id, data):
    db.session.query(CSharp_Challenge).filter_by(id=id).update(data)
    db.session.commit()
