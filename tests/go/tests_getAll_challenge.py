import os
import pytest
from app import db
from . import client,auth
from app.go.models_go import GoChallenge
import glob

path='public/challenges*'
def clean():
    path="public/challenges"
    for file in os.listdir(path):
        if (file.endswith(".go")):
            os.remove(os.path.join(path, file))

def add_new_challenge():
	challenge=GoChallenge(code="tests/go/files-for-tests/median.go",tests_code="tests/go/files-for-tests/median_test.go",repair_objective="repair",complexity="coplexity",best_score=100)
	db.session.add(challenge)
	db.session.commit()
	return challenge.id

def test_get_all_empty(client,auth):
    # arrange

    # act
    ret_get = client.get("/go/api/v1/go-challenges", headers={'Authorization': f'JWT {auth}'})
    ret_get_json=ret_get.json["challenges"]
    # downgrade
    for file in glob.glob(os.path.abspath(path)):
        if os.path.isfile(file):
            os.remove(file)
    # assert
    assert (ret_get_json=="not found")
    assert ret_get.status_code == 404

def test_get_all_working(client,auth):
    # arrange
    for i in range(0,3):
        add_new_challenge()
        
    
    # act
    ret_get = client.get("/go/api/v1/go-challenges", headers={'Authorization': f'JWT {auth}'})
    ret_get_json=ret_get.json["challenges"]
    # assert
    assert len(ret_get_json) == 3
    assert ret_get.status_code == 200