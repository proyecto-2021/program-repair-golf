import pytest
from app import create_app, db
from app.python.models import *
from . import client


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






