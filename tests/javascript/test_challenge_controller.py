from io import open_code
import pytest 
from app.javascript.controllers.challenge_controller import ChallengeController
from app.javascript.controllers.files_controller import get_directory, get_file, open_file
from app.javascript.models_js import *
from . import client 

def test_get_challenge_1(client):

    challenge = JavascriptChallenge(
        code = "tests/javascript/file_testing_folder/median.js",
        tests_code = "tests/javascript/file_testing_folder/median.test.js",
        repair_objective = "something",
        complexity = 0,
        best_score = 0,
    )
    
    db.session.add(challenge)
    db.session.commit()

    challenge_dict = challenge.to_dict()
    challenge_dict['code'] = open_file(challenge_dict['code'])
    challenge_dict['tests_code'] = open_file(challenge_dict['tests_code'])
    del challenge_dict['id']
    challenge_2 = ChallengeController.get_challenge(1)
    
    assert challenge_dict == challenge_2
    

def test_get_challenges(client):
    challenges = ChallengeController.get_challenges()
    assert challenges != []

@pytest.mark.skip(reason="needs improvement")
def test_create_challenge(client):
    challenge = ChallengeController.create_challenge(
        "tests/javascript/file_testing_folder/median.js",
        "tests/javascript/file_testing_folder/median.test.js",
        "repair_objective",
        0,
        "median",
        "median.test"
        )
    
    challenge_2 = ChallengeController.get_challenge(2)
    assert challenge_2 == challenge

@pytest.mark.skip(reason="needs improvement")
def test_update_challenge(client):
    challenge = ChallengeController.update_challenge(1,None,None,"yes",1,1)
    

    assert challenge != None

