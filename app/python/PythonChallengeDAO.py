from .. import db
from .PythonChallenge import PythonChallenge
from .models import PythonChallengeModel

class PythonChallengeDAO:

  def get_challenges():
    return PythonChallengeModel.query.all()

  def get_challenge(id):
    return PythonChallengeModel.query.filter_by(id = id).first()

  def create_challenge(challenge):
    new_challenge = PythonChallengeModel(code=challenge['code'],
      tests_code=challenge['tests_code'],
      repair_objective=challenge['repair_objective'],
      complexity=challenge['complexity'],
      best_score=0)

    db.session.add(new_challenge)
    db.session.commit()
    return new_challenge.id

  def get_repair_attempts(user_id, chellenge_id):
    return db.session.query(python_repair_attempt).filter_by(user_id = user_id, challenge_id = challenge_id).first()

  def increase_attempts(user_id, challenge_id):
    
    repair_attempts = PythonChallengeDAO.get_repair_attempts(user_id, challenge_id)
    cant_attempts = repair_attempts.attempts
    db.session.query(python_repair_attempt).filter_by(user_id = user_id, challenge_id = challenge_id).update(dict({'attempts': cant_attempts + 1}))
    db.session.commit()

  def update_best_score(id, score):
    
    challenge = PythonChallengeDAO.get_challenge(id)
    if challenge.best_score == 0 or score < challenge.best_score:
      db.session.query(PythonChallengeModel).filter_by(id=id).update(dict({'best_score': score}))
      db.session.commit()

  def update_challenge(id, new_data):
    db.session.query(PythonChallengeModel).filter_by(id=id).update(dict(new_data))
    db.session.commit()