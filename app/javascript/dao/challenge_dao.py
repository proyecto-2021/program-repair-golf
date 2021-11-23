from app.javascript.exceptions.challenge_dao_exception import challenge_dao_exception
from ..models_js import JavascriptChallenge, db

class ChallengeDAO():
    
    def get_challenge(id):
        challenge = JavascriptChallenge.query.filter(id == JavascriptChallenge.id).first()
        if not challenge: 
            raise challenge_dao_exception(f'the id does not exist or is null',challenge_dao_exception.HTTP_NOT_FOUND)  
        return challenge
        
    def get_all_challenges():
        challenges = JavascriptChallenge.query.all()
        return challenges

    def save_challenge(code, test_code, repair_objective,complexity,best_score):
        challenge = JavascriptChallenge(code = code,
                                        tests_code = test_code,
                                        repair_objective = repair_objective,
                                        complexity = complexity,
                                        best_score = best_score)
        db.session.add(challenge)
        db.session.commit()
        return challenge

    def update_challenge(id, code, test_code, repair_objective, complexity, best_score):
      
        challenge = ChallengeDAO.get_challenge(id)
        if code:
            challenge.code = code
        if test_code:
            challenge.test_code = test_code
        if repair_objective:
            challenge.repair_objective = repair_objective
        if complexity:
            challenge.complexity = complexity
        if best_score:
            challenge.best_score = best_score
        db.session.commit()
        return challenge

    def delete_challenge(id):
        challenge = ChallengeDAO.get_challenge(id)
        db.session.delete(challenge)
        db.session.commit()
        return challenge