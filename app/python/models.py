from .. import db

class PythonChallengeModel(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  code = db.Column(db.String(256), nullable=False)
  tests_code = db.Column(db.String(256), nullable=False)
  repair_objective = db.Column(db.String(120), nullable=False)
  complexity = db.Column(db.Integer, nullable=False)
  best_score = db.Column(db.Integer, nullable=True)

  #takes a row and returns it as a dictionary
  def to_dict(self):
    row_as_dict = self.__dict__                    #we turn the row into a dict
    row_as_dict.pop('_sa_instance_state', None)  #we remove unnecesary data
    return row_as_dict