from app.javascript.exceptions.challenge_dao_exception import challenge_dao_exception
from ..models_js import JavascriptChallenge, db


def get_challenge(id):
    challenge = JavascriptChallenge.query.filter(id == JavascriptChallenge.id).first()
    if challenge == None: 
        raise challenge_dao_exception(f'the id does not exist or is null',challenge_dao_exception.HTTP_NOT_FOUND)  
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
    challenge = JavascriptChallenge.query.filter(id==JavascriptChallenge.id).first()
    if challenge == None:
        raise challenge_dao_exception(f'the id does not exist or is null',challenge_dao_exception.HTTP_NOT_FOUND)
    db.session.delete(challenge)
    db.session.commit()
    return challenge
