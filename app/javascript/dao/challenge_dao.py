from app.javascript.exceptions.dao_get_challenge_exception import dao_get_challenge_exception
from ..models_js import JavascriptChallenge, db


def get_challenge(id):
    challenge = JavascriptChallenge.query.filter_by(id==JavascriptChallenge.id).first()
    if challenge == None: 
        raise dao_get_challenge_exception(f'the id does not exist or is null',dao_get_challenge_exception.HTTP_NOT_FOUND)  
    return challenge
    

def get_all_challenges():
    challenges = JavascriptChallenge.query.all()
    return challenges

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
