from app import create_app, db
from app.java import challenge
import pytest
from app.java.models_java import Challenge_java
from app.java.DAO_java_challenge import DAO_java_challenge
from . import client
from app.java.views import *

#Create Challenge

def create_dict(code, test, repair, complexity):
    dict = {"source_code_file_name": code,
        "test_suite_file_name": test,
        "repair_objective": repair,
        "complexity": complexity
        }
    return dict


def test_get_not_exist_id(client):
    code1 = "code1"
    test1 = "test1"
    repair = "repair"
    complexity = "1"
    dict = create_dict(code1, test1, repair, complexity)

    DAO_java_challenge.create_challenge(dict)
    challenge = DAO_java_challenge.challenges_id_java(2)
    aux = DAO_java_challenge.challenges_id_java(1)
    resp = Challenge_java.__repr__(aux)
    db.session.delete(aux)
    db.session.commit()
    assert challenge is None
    assert resp is not None
    assert resp['code'] == code1

def test_post(client):
    code1 = "code1"
    test1 = "test1"
    repair = "repair"
    complexity = "2"
    dict = create_dict(code1, test1, repair, complexity)

    DAO_java_challenge.create_challenge(dict)
    challenge = DAO_java_challenge.challenges_id_java(1)
    resp = Challenge_java.__repr__(challenge)
    db.session.delete(challenge)
    db.session.commit()

    assert resp['code'] == code1
    assert resp['tests_code'] == test1
    assert resp['repair_objective'] == repair
    assert int(resp['complexity']) == 2
    assert resp['best_score'] == 500

def test_post_many_loads(client):
    code1 = "code1"
    test1 = "test1"
    repair = "repair"
    complexity = "1"
    dict = create_dict(code1, test1, repair, complexity)

    code2 = "code2"
    test2 = "test2"
    repair2 = "repair2"
    complexity2 = "2"
    dict2 = create_dict(code2, test2, repair2, complexity2)

    code3 = "code3"
    test3 = "test3"
    repair3 = "repair3"
    complexity3 = "3"
    dict3 = create_dict(code3, test3, repair3, complexity3)

    code4 = "code4"
    test4 = "test4"
    repair4 = "repair4"
    complexity4 = "4"
    dict4 = create_dict(code4, test4, repair4, complexity4)

    DAO_java_challenge.create_challenge(dict)
    DAO_java_challenge.create_challenge(dict2)
    DAO_java_challenge.create_challenge(dict3)
    DAO_java_challenge.create_challenge(dict4)

    resp1 = {"challenges":[]}
    resp1['challenges'] = DAO_java_challenge.all_challenges_java()
    p = DAO_java_challenge.challenges_id_java(4)
    t = DAO_java_challenge.challenges_id_java(3)
    p1 = Challenge_java.__repr__(p)
    t1 = Challenge_java.__repr__(t)

    for c in resp1["challenges"]:
        db.session.delete(c)
        db.session.commit()
     
    assert len(resp1["challenges"]) == 4
    assert p1['id'] == 4
    assert p1['code'] == code4
    assert t1['repair_objective'] == repair3

def test_post_same_name(client):
    code1 = "code1"
    test1 = "test1"
    repair = "repair"
    complexity = "1"
    dict = create_dict(code1, test1, repair, complexity)

    code2 = "code1"
    test2 = "test1"
    repair2 = "repair"
    complexity2 = "1"
    dict2 = create_dict(code2, test2, repair2, complexity2)

    DAO_java_challenge.create_challenge(dict)
    try:
        DAO_java_challenge.create_challenge(dict2)
    except Exception as e:
        assert str(e) == "Name of the code exist"

def test_put_ok(client):
    code = "code"
    test = "test"
    repair = "repair"
    complexity = "1"

    dict = create_dict(code, test, repair, complexity)

    DAO_java_challenge.create_challenge(dict)
    
    repair_upd="make all pass"
    complexity_upd=3
    code_upd="prueba"
    test_code_upd="testpasado"

    challenge_old = DAO_java_challenge.challenges_id_java(1)
    resp = Challenge_java.__repr__(challenge_old)

    challenge_old.repair_objective= repair_upd
    challenge_old.complexity=complexity_upd
    challenge_old.code=code_upd
    challenge_old.tests_code=test_code_upd
   
    DAO_java_challenge.updatechallenge(challenge_old)
    
    challenge_upd = DAO_java_challenge.challenges_id_java(1)
    resp1 = Challenge_java.__repr__(challenge_upd)

    db.session.delete(challenge_old)
    db.session.delete(challenge_upd)
    db.session.commit()

    assert resp['repair_objective'] == repair
    assert int(resp['complexity']) == 1
    assert resp['code'] == code 
    assert resp['tests_code'] == test

    assert resp1['repair_objective'] == repair_upd
    assert int(resp1['complexity']) == 3
    assert resp1['code'] == code_upd
    assert resp1['tests_code'] == test_code_upd

def test_put_notOK(client):
    code = "code"
    test = "test"
    repair = "repair"
    complexity = "1"

    dict = create_dict(code, test, repair, complexity)

    DAO_java_challenge.create_challenge(dict)
    challenge_old = DAO_java_challenge.challenges_id_java(1)
    resp = Challenge_java.__repr__(challenge_old)
    
    repair_upd="make all pass"
    complexity_upd=3
    code_upd="prueba"
    test_code_upd="testpasado"
    
    try:
        challenge_upd = DAO_java_challenge.challenges_id_java(2)
    except Exception as e:
        assert str(e) == "Challenge not found"
    
   
    db.session.delete(challenge_old)
    db.session.commit()

    assert challenge_upd is None
    assert resp is not None
   