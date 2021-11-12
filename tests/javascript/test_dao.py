import pytest

from . import client
from app.javascript.models_js import *
from app.javascript.dao.challenge_dao import ChallengeDAO 

def test_get_all_challenges(client):
    empty_list = ChallengeDAO.get_all_challenges()
    assert empty_list == []   

def test_get_challenge_1(client):
    challenge = JavascriptChallenge(
        code = "empty code",
        tests_code = "empty test",
        repair_objective = "something",
        complexity = 0,
        best_score = 0,
    )
    
    db.session.add(challenge)
    db.session.commit()

    challenge_2 = ChallengeDAO.get_challenge(1)
    assert challenge == challenge_2

def test_get_challenge_exception_raise(client):
    with pytest.raises(Exception):
        ChallengeDAO.get_challenge(5)

def test_delete_challenge(client):
    challenge = JavascriptChallenge(
        code = "empty code",
        tests_code = "empty test",
        repair_objective = "something",
        complexity = 0,
        best_score = 0,
    )
    
    db.session.add(challenge)
    db.session.commit()

    challenge_delete = ChallengeDAO.delete_challenge(2)
    assert challenge == challenge_delete


def test_save_challenge(client):
        
    challenge_save = ChallengeDAO.save_challenge("algo","algo test","algo2",0,0) 
    challenge = ChallengeDAO.get_challenge(challenge_save.id)
    assert challenge == challenge_save

def test_update_challenge(client):

    challenge_update = ChallengeDAO.update_challenge(1,"algo","algo test","algo2",0,0)
    challenge = ChallengeDAO.get_challenge(challenge_update.id)
    assert challenge == challenge_update
        
        

def test_update_challenge1(client):

    challenge_update = ChallengeDAO.update_challenge(1,None,None,None,2,5)
    challenge = ChallengeDAO.get_challenge(challenge_update.id)
    assert challenge == challenge_update
        

   
