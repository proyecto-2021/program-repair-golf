import pytest
import json
from . import client, auth 
from . __init__ import createChallenge, create_challenge_update,  post_generator,remove_files, ChallengeDAO
from . import db
from app.javascript.models_js import JavascriptChallenge

url = 'javascript/javascript-challenges'

def test_put(client, auth):
    # arrange
    challeng_new = createChallenge("median", "median.test", "test", '1')
    create = client.post(url, data=challeng_new, headers={'Authorization': f'JWT {auth}'})
    challenge_json = create.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    challenge_upd = create_challenge_update("median", "median.test", "test update", '3','20')
    # act
    update = client.put(f"{url}/{challenge_id}",data=challenge_upd, headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)

    # assert
    assert update.status_code == 200

def test_put_not_data(client, auth):
    # arrange
    challeng_new = createChallenge("median", "median.test", "test", '1')
    create = client.post(url, data=challeng_new, headers={'Authorization': f'JWT {auth}'})
    challenge_json = create.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    challenge_upd = create_challenge_update("median", "median.test", "test update", '3','20')
    challenge_upd['source_code_file'] = None
    # act
    update = client.put(f"{url}/{challenge_id}",data=None, headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)

    # assert
    assert update.status_code == 404

def test_put_not_file(client, auth):
    challeng_new = createChallenge("median", "median.test", "test", '1')
    create = client.post(url, data=challeng_new, headers={'Authorization': f'JWT {auth}'})
    challenge_json = create.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    remove_files(challenge.code, challenge.tests_code)
    data = create_challenge_update("median", "median.test", "test update", '3','20')
    # act
    update = client.put(f"{url}/{challenge_id}",data=data, headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)

    # assert
    assert update.status_code == 404

def test_put_challenge_not_exist(client, auth):
    challeng_new = createChallenge("median", "median.test", "test", '1')
    create = client.post(url, data=challeng_new, headers={'Authorization': f'JWT {auth}'})
    challenge_json = create.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    challenge_upd = create_challenge_update("median", "median.test", "test update", '3','20')
    # act
    update = client.put(f"{url}/{9999999}",data=challenge_upd, headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)

    # assert
    assert update.status_code == 404

def test_put_not_compile(client, auth):
    challeng_new = createChallenge("median", "median.test", "test", '1')
    create = client.post(url, data=challeng_new, headers={'Authorization': f'JWT {auth}'})
    challenge_json = create.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    challenge_upd = create_challenge_update("median_not_compile", "median.test", "test update", '3','20')
    # act
    update = client.put(f"{url}/{challenge_id}",data=challenge_upd, headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)

    # assert
    assert update.status_code == 404

def test_put_pass_test(client, auth):
    challeng_new = createChallenge("median", "median.test", "test", '1')
    create = client.post(url, data=challeng_new, headers={'Authorization': f'JWT {auth}'})
    challenge_json = create.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    challenge_upd = create_challenge_update("example_pass_t", "example_pass_t.test", "test update", '3','20')
    # act
    update = client.put(f"{url}/{challenge_id}",data=challenge_upd, headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)

    # assert
    assert update.status_code == 404 

def test_token_not_valid(client):
    #arrange
    data = createChallenge('median','median.test','Objective is hshshs', '3')
    auth = 'Token not valid'
    #act
    result = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data)
    #assert
    assert result.status_code == 401


def test_authentication_required(client):
    #arrange
    data = createChallenge('median','median.test', 'Objective is hshshs', '3')
    #act
    result = client.post('/javascript/javascript-challenges',data=data)
    #assert
    assert result.status_code == 401