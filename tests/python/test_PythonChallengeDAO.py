from app import create_app, db
from app.python.models import *
from app.python.PythonChallengeDAO import PythonChallengeDAO
from . import client

def test_DAO_saves_challenge(client):
  #arrange
  len_before_post = len(PythonChallengeDAO.get_challenges())

  new_challenge = {
    'code': 'code',
    'tests_code': 'test_path',
    'repair_objective': 'Make all tests pass.',
    'complexity': '1'}

  PythonChallengeDAO.create_challenge(new_challenge)

  assert len(PythonChallengeDAO.get_challenges()) == len_before_post + 1

def test_DAO_saves_challenge_correctly(client):
  #arrange
  new_challenge = {
    'code': 'code',
    'tests_code': 'test_path',
    'repair_objective': 'Make all tests pass.',
    'complexity': '1'}

  challenge_id = PythonChallengeDAO.create_challenge(new_challenge)
  challenge_db = PythonChallengeDAO.get_challenge(challenge_id)
  
  assert new_challenge['code'] == challenge_db.code
  assert new_challenge['tests_code'] == challenge_db.tests_code
  assert new_challenge['repair_objective'] == challenge_db.repair_objective
  assert new_challenge['complexity'] == str(challenge_db.complexity)
  assert 0 == challenge_db.best_score

#testing of update field complexity
def test_DAO_update_some_fields(client):
  #arrange
  new_challenge = {
    'code': 'code',
    'tests_code': 'test_path',
    'repair_objective': 'Make all tests pass.',
    'complexity': '1'}
  #post challenge to be updated
  challenge_id = PythonChallengeDAO.create_challenge(new_challenge)

  challenge_update = {
    'tests_code': 'new_test_path',
    'complexity': '10'}

  PythonChallengeDAO.update_challenge(challenge_id, challenge_update)
  challenge_db = PythonChallengeDAO.get_challenge(challenge_id)

  assert new_challenge['code'] == challenge_db.code
  assert challenge_update['tests_code'] == challenge_db.tests_code
  assert new_challenge['repair_objective'] == challenge_db.repair_objective
  assert challenge_update['complexity'] == str(challenge_db.complexity)

def test_DAO_updates_all_fields(client):
  #arrange
  new_challenge = {
    'code': 'code',
    'tests_code': 'test_path',
    'repair_objective': 'Make all tests pass.',
    'complexity': '1'}
  #post challenge to be updated
  challenge_id = PythonChallengeDAO.create_challenge(new_challenge)

  challenge_update = {
    'code': 'new_code',
    'tests_code': 'new_test_path',
    'repair_objective': 'Updating everything.',
    'complexity': '55'}

  PythonChallengeDAO.update_challenge(challenge_id, challenge_update)
  challenge_db = PythonChallengeDAO.get_challenge(challenge_id)

  assert challenge_update['code'] == challenge_db.code
  assert challenge_update['tests_code'] == challenge_db.tests_code
  assert challenge_update['repair_objective'] == challenge_db.repair_objective
  assert challenge_update['complexity'] == str(challenge_db.complexity)
