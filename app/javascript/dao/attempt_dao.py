from ..models_js import javascript_attempts, JavascriptChallenge, db
from app.auth.userdao import get_user_by_id

class AttemptsDAO():
    def create_attempt(self, challenge_id, user_id):
        challenge_attempts = self.get_attempts(challenge_id, user_id)
        if challenge_attempts is None:
            challenge = db.session.query(JavascriptChallenge).filter_by(id=challenge_id).first()
            user = get_user_by_id(user_id)
            challenge.users_attempts.append(user) 
            db.session.commit()
        attempts = self.get_attempts_count(challenge_id, user_id)
        db.session.query(javascript_attempts).filter_by(challenge_id=challenge_id, user_id=user_id).update({'count': attempts+1})
        db.session.commit()


    def get_attempts(self, challenge_id, user_id):
        return db.session.query(javascript_attempts).filter_by(challenge_id=challenge_id, user_id=user_id).first()

    def get_attempts_count(self, challenge_id, user_id):
        return self.get_attempts(challenge_id, user_id).count