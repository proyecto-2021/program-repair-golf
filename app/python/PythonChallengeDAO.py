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

  def update_challenge(id, new_data):
    db.session.query(PythonChallengeModel).filter_by(id=id).update(dict(new_data))
    db.session.commit()