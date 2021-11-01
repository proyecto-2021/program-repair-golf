from app import db

class RubyChallenge(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(256)) #Path to source file
    tests_code = db.Column(db.String(256)) #Path to test suite file
    repair_objective = db.Column(db.String(128))
    complexity = db.Column(db.String(3))
    best_score = db.Column(db.Integer())

    def get_dict(self):
        return {
            "id":self.id,
            "code":self.code,
            "tests_code":self.tests_code,
            "repair_objective":self.repair_objective,
            "complexity":self.complexity,
            "best_score":self.best_score
        }

    def get_data(self):
        with open(self.code) as f1:
            code_content = f1.read()
        with open(self.tests_code) as f2:
            tests_code_content = f2.read()

        return {
            "id":self.id,
            "code":code_content,
            "tests_code":tests_code_content,
            "repair_objective":self.repair_objective,
            "complexity":self.complexity,
            "best_score":self.best_score
        }

def get_challenge(id):
    return db.session.query(RubyChallenge).filter_by(id=id).first().get_dict()

def get_challenges():
    return [challenge.get_dict() for challenge in db.session.query(RubyChallenge).all()]

def create_challenge(code, tests_code, repair_objective, complexity):
    challenge = RubyChallenge(
        code = code,
        tests_code = tests_code,
        repair_objective = repair_objective,
        complexity = complexity,
        best_score = 0
    )
    db.session.add(challenge)
    db.session.commit()
    return challenge.get_dict()

def update_challenge(id, changes):
    if len(changes) == 0:
        return 1
    result = db.session.query(RubyChallenge).filter_by(id=id).update(changes)
    db.session.commit()
    return result

def exists(id):
    return get_challenge(id) is not None
