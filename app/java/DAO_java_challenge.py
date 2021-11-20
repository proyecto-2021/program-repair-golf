from app.java.models_java import Challenge_java, java_attempts
#from . import java
from app import db
from app.auth.userdao import get_user_by_id

class DAO_java_challenge():

    def all_challenges_java():
        return Challenge_java.query.all()
    
    def challenges_id_java(id):
        return Challenge_java.query.filter_by(id=id).first()

    def get_challenge_by_code(code_file_name):
        return Challenge_java.query.filter_by(code=code_file_name).first()

    def create_challenge(dict):
        challenge = DAO_java_challenge.get_challenge_by_code(dict['source_code_file_name'])
        if challenge is None:
            if int(dict['complexity']) <= 5:
                new_chan = Challenge_java(code = dict['source_code_file_name'],
                    tests_code = dict['test_suite_file_name'],
                    repair_objective = dict['repair_objective'],
                    complexity = dict['complexity'],
                    score = 500)
                db.session.add(new_chan)
                db.session.commit()
            else:
                raise Exception("The complexity is greater than 5, it must be less than equal to 5")
        else:
           raise Exception("Name of the code exist")

    def updatechallenge(challenge):
        challenge_n = DAO_java_challenge.challenges_id_java(challenge.id)
        if challenge_n is not None:
           db.session.commit()
        else:
           raise Exception("Id Challenge Not Found!")

    def update(challenge):
        db.session.add(challenge)
        db.session.commit()

    def get_attempts(challenge_id, user_id):
        return db.session.query(java_attempts).filter_by(challenge_id=challenge_id, user_id=user_id).first()

    def get_cant_attempts(challenge_id, user_id):
        return db.session.query(java_attempts).filter_by(challenge_id=challenge_id, user_id=user_id).first().attempts

    def create_attempts_by_user(challenge_id, user_id):
        challenge = DAO_java_challenge.get_attempts(challenge_id, user_id)
        if challenge is None:
            user = get_user_by_id(user_id)
            curr_challenge = db.session.query(Challenge_java).filter_by(id=challenge_id).first()
            curr_challenge.attempts_by_users.append(user) 
            db.session.add(curr_challenge)
            db.session.commit()
        attempts = DAO_java_challenge.get_cant_attempts(challenge_id, user_id)
        db.session.query(java_attempts).filter_by(challenge_id=challenge_id, user_id=user_id).update({'attempts': attempts+1})
        db.session.commit()