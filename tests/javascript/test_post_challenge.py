import pytest
from . import client, auth 
from . __init__ import createChallenge,remove_files, ChallengeDAO
from . import db
from app.javascript.models_js import JavascriptChallenge


def test_post_challenge(client, auth):
    #arrange
    data = createChallenge('median', 'median.test', 'Testing', '1')
    #act
    result = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data)
    challenge_json = result.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    remove_files(challenge.code, challenge.tests_code)
    #assert
    assert result.status_code == 200


def test_challenge_exist(client, auth):
    #arrange
    data1 = createChallenge('median', 'median.test', 'Testing', '1')
    data2 = createChallenge('median', 'median.test', 'Testing', '1')  
    #act
    result1 = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data1)
    result2 = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data2)   
    challenge_json = result1.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    remove_files(challenge.code, challenge.tests_code)
    #assert
    assert result2.status_code == 409


def test_file_not_compile(client,auth):
    #arrange
    data = createChallenge('medianNcp','median.test', 'dsdsd','4')
    #act
    result = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data)
    #assert
    assert result.status_code == 404


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