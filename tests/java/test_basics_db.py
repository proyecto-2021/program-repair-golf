from app import create_app, db
import pytest
from app.java.models_java import Challenge_java
from app.java.DAO_java_challenge import DAO_java_challenge
from . import client
from app.java.views import *

#Create Challenge
#def test_new_challenge(client):
def test_ViewAllChallenges(client):
    challenge = {"challenges":[]}
    challenge ['challenges'] = DAO_java_challenge.all_challenges_java()
    resp = len(challenge)
    assert resp == 1

    #verrrrrrrrrrrrrrrrrrrrrrrrrrrr 
    '''
    challenge = Challenge_java(code='source_code_file_name', tests_code='test_suite_file_name', repair_objective='repair_objective', complexity='complexity', score=500)
    for j in range (5):  
        DAO_java_challenge.create_challenge(challenge)
    challenge ['challenges'] = DAO_java_challenge.all_challenges_java()
    assert resp == 6
    '''

def test_ViewChallenges(client):
    challenge = {"challenges":[]}
    id=1
    challenge ['challenges'] = DAO_java_challenge.challenges_id_java(id)
    resp = len(challenge)
    assert resp == 1 

def test_post(client):
    code1 = "code1"
    test1 = "test1"
    repair = "repair"
    complexity = "complexity"

    dict = {"source_code_file_name": code1,
        "test_suite_file_name": test1,
        "repair_objective": repair,
        "complexity": complexity
        }
    DAO_java_challenge.create_challenge(dict)
    challenge = DAO_java_challenge.challenges_id_java(1)
    resp = Challenge_java.__repr__(challenge)
    db.session.delete(challenge)
    db.session.commit()
    assert resp['code'] == code1
    assert resp['tests_code'] == test1
    assert resp['repair_objective'] == repair
    assert resp['complexity'] == complexity
    assert resp['best_score'] == 500

def test_post_for(client):
    code1 = "code1"
    test1 = "test1"
    repair = "repair"
    complexity = "complexity"
    dict = {"source_code_file_name": code1,
        "test_suite_file_name": test1,
        "repair_objective": repair,
        "complexity": complexity
        }
    code2 = "code2"
    test2 = "test2"
    repair2 = "repair2"
    complexity2 = "complexity2"
    dict2 = {"source_code_file_name": code2,
        "test_suite_file_name": test2,
        "repair_objective": repair2,
        "complexity": complexity2
        }
    code3 = "code3"
    test3 = "test3"
    repair3 = "repair3"
    complexity3 = "complexity3"
    dict3 = {"source_code_file_name": code3,
        "test_suite_file_name": test3,
        "repair_objective": repair3,
        "complexity": complexity3
        }
    code4 = "code4"
    test4 = "test4"
    repair4 = "repair4"
    complexity4 = "complexity4"
    dict4 = {"source_code_file_name": code4,
        "test_suite_file_name": test4,
        "repair_objective": repair4,
        "complexity": complexity4
        }
    DAO_java_challenge.create_challenge(dict)
    DAO_java_challenge.create_challenge(dict2)
    DAO_java_challenge.create_challenge(dict3)
    DAO_java_challenge.create_challenge(dict4)

    resp1 = {"challenges":[]}
    resp1['challenges'] = DAO_java_challenge.all_challenges_java()
    p = DAO_java_challenge.challenges_id_java(4)
    p1 = Challenge_java.__repr__(p)

    for c in resp1["challenges"]:
        db.session.delete(c)
        db.session.commit()
     
    assert len(resp1["challenges"]) == 4
    assert p1['id'] == 4
    assert p1['code'] == code4

def test_post_exist(client):
    code1 = "code1"
    test1 = "test1"
    repair = "repair"
    complexity = "complexity"
    dict = {"source_code_file_name": code1,
        "test_suite_file_name": test1,
        "repair_objective": repair,
        "complexity": complexity
        }
    code2 = "code1"
    test2 = "test1"
    repair2 = "repair"
    complexity2 = "complexity"
    dict2 = {"source_code_file_name": code2,
        "test_suite_file_name": test2,
        "repair_objective": repair2,
        "complexity": complexity2
        }
    DAO_java_challenge.create_challenge(dict)
    try:
        DAO_java_challenge.create_challenge(dict2)
    except Exception as e:
        assert str(e) == "Name of the code exist"