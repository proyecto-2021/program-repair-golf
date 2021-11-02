from ..models_js import JavascriptChallenge, db

def get_challenge(id):
    return JavascriptChallenge.query.filter_by(id==JavascriptChallenge.id).first()

def get_all_challenges():
    return JavascriptChallenge.query.all()

def save_challenge(code, test_code, repair_objective,complexity,best_score):
    challenge = JavascriptChallenge(code,test_code,repair_objective,complexity,best_score)
    db.session.add(challenge)
    db.session.commit()
    return challenge

def delete_challenge(id):
    challenge = JavascriptChallenge.query.filter_by(id==JavascriptChallenge.id).first()
    db.session.delete(challenge)
    db.session.commit()
    return challenge
