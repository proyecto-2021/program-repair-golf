import pytest
from app import create_app, db
from app.python.models import *
from . import client

#testing of Saved challenge
def test_db_saved_data(client):
  #arrange
  new_challenge = PythonChallenge(
      code='code',
      tests_code='test_path',
      repair_objective= "Make all tests pass.",
      complexity= "1",
      best_score=0)
  
  db.session.add(new_challenge)
  db.session.commit()
  
  assert len(PythonChallenge.query.all()) > 0

#testing of delete challenge
def test_db_delete_all_data(client):
  
  db.session.query(PythonChallenge).delete()
  db.session.commit()

  lengDbBefore = len(PythonChallenge.query.all())
  
  new_challenge = PythonChallenge(
      code='code',
      tests_code='test_path',
      repair_objective= "Make all tests pass.",
      complexity= "1",
      best_score=0)
  
  db.session.add(new_challenge)
  db.session.commit()

  db.session.query(PythonChallenge).filter(PythonChallenge.id == new_challenge.id).delete()
  db.session.commit()
  
  assert len(PythonChallenge.query.all()) == lengDbBefore

#testing of update field complexity
def test_db_update_field(client):
  
  db.session.query(PythonChallenge).delete()
  db.session.commit()

  new_challenge = PythonChallenge(
      code='code',
      tests_code='test_path',
      repair_objective= "Make all tests pass.",
      complexity= "1",
      best_score=0)
  
  db.session.add(new_challenge)
  db.session.commit()

  db.session.query(PythonChallenge).filter(PythonChallenge.id == new_challenge.id).update(dict( complexity = "100") )
  db.session.commit()

  db.session.query(PythonChallenge).filter(PythonChallenge.id == new_challenge.id).update(dict( best_score = 32 ) )
  db.session.commit()

  db.session.query(PythonChallenge).filter(PythonChallenge.id == new_challenge.id).update(dict( repair_objective = "testing field" ) )
  db.session.commit()

  
  complexityRes = PythonChallenge.query.filter_by(complexity = "100" ).first()
  
  assert complexityRes.complexity == 100
  assert complexityRes.best_score == 32
  assert complexityRes.repair_objective == "testing field"

  

