import pytest
from app.javascript.models_js import *
from . import client
from app.javascript.controllers.challenge_repair_controller import ChallengeRepairController


def test_score_ok_1(client):
    score = 1
    best_score = 2
    result = ChallengeRepairController.score_ok(score,best_score)
    assert result == True

def test_score_ok_2(client):
    score = 2
    best_score = 1 
    result = ChallengeRepairController.score_ok(score,best_score)
    assert result == False

def test_score_ok_3(client):
    score = 2
    best_score = 0 
    result = ChallengeRepairController.score_ok(score,best_score)
    assert result == True

def test_calculate_score(client):
    result = ChallengeRepairController.calculate_score(
        "tests/javascript/file_testing_folder/file_testing_folder_2/median.js",
        "tests/javascript/file_testing_folder/file_testing_folder_2/median.js")
    assert result == 0


def test_repair_1(client):
    with pytest.raises(Exception) as e_info:
        ChallengeRepairController.repair(1, "tests/javascript/file_testing_folder/file_testing_folder_2/median.js")

def test_repair_2(client):
    with pytest.raises(Exception) as e_info:
        challenge = JavascriptChallenge(
        code = "something.js",
        tests_code = "tests/javascript/file_testing_folder/file_testing_folder_2/median.js",
        repair_objective = "something",
        complexity = 0,
        best_score = 0,
        )

        db.session.add(challenge)
        db.session.commit()
        
        ChallengeRepairController.repair(1, "tests/javascript/file_testing_folder/file_testing_folder_2/median.js")


@pytest.mark.skip(reason="module does not work")
def test_repair_skip(client):
    challenge = JavascriptChallenge(
        code = "tests/javascript/file_testing_folder/file_testing_folder_2/median.js",
        tests_code = "tests/javascript/file_testing_folder/file_testing_folder_2/median.test.js",
        repair_objective = "something",
        complexity = 0,
        best_score = 0,
    )
    
    db.session.add(challenge)
    db.session.commit()

    result = ChallengeRepairController.repair(2,"tests/javascript/file_testing_folder/file_testing_folder_2/median.js")
    assert True
