from .rubychallengemodel import RubyChallengeModel, ruby_attempts
from app.auth.userdao import get_user_by_id
from app import db


class RubyChallengeDAO(object):
    """Manage RubyChallenge in database."""
    def __init__(self):
        pass

    def get_challenge(self, challenge_id):
        """Retrieve a challenge from database.
        
        Parameters:
            challenge_id (int): id of the challenge that will be retrieved.
        """
        challenge = db.session.query(RubyChallengeModel).filter_by(id=challenge_id).first().get_dict()
        del challenge['id']
        return challenge

    def get_challenges(self):
        """Retrieve all challenges from database."""
        return [challenge.get_dict() for challenge in db.session.query(RubyChallengeModel).all()]

    def create_challenge(self, code, tests_code, repair_objective, complexity):
        """Create a new challenge in database.
        
        Parameters:
            code (String): path where code is stored,
            tests_code (String): path where test suite is stored,
            repair_objective (String): objective of the challenge,
            complexity (String): complexity of the challenge.
        """
        challenge = RubyChallengeModel(
            code=code,
            tests_code=tests_code,
            repair_objective=repair_objective,
            complexity=complexity,
            best_score=0
        )
        db.session.add(challenge)
        db.session.commit()
        return challenge.get_dict()['id']

    def update_challenge(self, challenge_id, changes):
        """Update a challenge in the database.
        
        Parameters:
            challenge_id (int): id of the challenge to update,
            changes (dict): dictionary containing all changes to be made.
        """
        db.session.query(RubyChallengeModel).filter_by(id=challenge_id).update(changes)
        db.session.commit()

    def exists(self, challenge_id):
        """Check if a challenge exists in the database.
        
        Parameters:
            challenge_id (int): id of the challenge to check existence.
        """
        return db.session.query(RubyChallengeModel).filter_by(id=challenge_id).first() is not None

    def add_attempt(self, challenge_id, user_id):
        """Add a new attempt in the ruby_attempts table.
        
        Parameters:
            challenge_id (int): id of the challenge being attempted,
            user_id (int): id of the user making the attempt.
        """
        challenge_attempts = self.get_attempts(challenge_id, user_id)
        if challenge_attempts is None:
            challenge = db.session.query(RubyChallengeModel).filter_by(id=challenge_id).first()
            user = get_user_by_id(user_id)
            challenge.users_attempts.append(user) 
            db.session.commit()
        attempts = self.get_attempts_count(challenge_id, user_id)
        db.session.query(ruby_attempts).filter_by(challenge_id=challenge_id, user_id=user_id) \
            .update({'count': attempts+1})
        db.session.commit()

    def get_attempts(self, challenge_id, user_id):
        """Retrieve the attempt row defined by parameters.
        
        Parameters:
            challenge_id (int): id of the challenge related to retrieve,
            user_id (int): id of the user related to retrieve.
        """
        return db.session.query(ruby_attempts).filter_by(challenge_id=challenge_id, user_id=user_id).first()

    def get_attempts_count(self, challenge_id, user_id):
        """Retrieve the count of attempts for given challenge and user.
        
        Parameters:
            challenge_id (int): id of the challenge related to retrieve,
            user_id (int): id of the user related to retrieve.
        """
        return self.get_attempts(challenge_id, user_id).count
