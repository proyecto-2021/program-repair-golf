import pytest
from . import client
from app.javascript.models_js import *

def test_empty_db(client):
    empty_list = JavascriptChallenge().query.all()
    assert empty_list == []


def test_create_challenge(client):
    challenge = JavascriptChallenge(
        code = "empty code",
        tests_code = "empty test",
        repair_objective = "something",
        complexity = 0,
        best_score = 0,
    )
    
    db.session.add(challenge)
    db.session.commit()

    assert JavascriptChallenge.query.all() != []   


def test_to_dict(client):

    challenge = JavascriptChallenge.query.first()
    
   
    challenge_dict = {
        "id" : 1,
        "code" : "empty code",
        "tests_code" : "empty test",
        "repair_objective" : "something",
        "complexity" : 0,
        "best_score" : 0,
     }
    

    assert challenge.to_dict() == challenge_dict   

def test_to_dict_unequals(client):
    challenge = JavascriptChallenge.query.first()
    
    challenge_dict = {
        "id" : 2,
        "code" : "not empty code",
        "tests_code" : "not empty test",
        "repair_objective" : "else something",
        "complexity" : 1,
        "best_score" : 1,
     }
    

    assert challenge.to_dict() != challenge_dict

