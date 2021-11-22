import pytest
from . import client, auth 
from . __init__ import createChallenge, remove_files, ChallengeDAO
from . import db
from app.javascript.models_js import JavascriptChallenge



#Test de id de challenge invalido
def test_challenge_id_not_valid(client,auth):
    #arrange
    url = '/javascript-challenges/9999999'
    #act
    resp = client.get(url, headers={'Authorization': f'JWT {auth}'})
    #assert
    assert resp.status_code == 404
    #assert resp.json['error'] == 'Id challenge not exist'
    
def test_get_javascript(client,auth):
    #arrange
	url = '/javascript-challenges'
	#act
	resp = client.get(url, headers={'Authorization': f'JWT {auth}'})
	res = resp.json
	#assert
	assert resp.status_code == 404

def test_get_after_post(client, auth):
    #arrange
    data = createChallenge('median', 'median.test', 'Testing', '3')
    result = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data)
    
    challenge_json = result.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    #act
    res = client.get(f'javascript/javascript-challenges/{challenge_id}', headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)
    #assert
    assert res.status_code == 200 
    
def test_token_not_valid_id(client):
    #arrange
    authNot = 'Tokennotvalid'
    #act
    result = client.get(f'javascript/javascript-challenges/1', headers={'Authorization': f'JWT {authNot}'})
    #assert
    assert result.status_code == 401

def test_token_not_valid_all(client):
    #arrange
    authNot = 'Tokennotvalid'
    #act
    result = client.get(f'javascript/javascript-challenges/', headers={'Authorization': f'JWT {authNot}'})
    #assert
    assert result.status_code == 401 

def test_authentication_required(client, auth):
    #arrange
    data = createChallenge('median', 'median.test', 'Testing', '1')
    result = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data)
    challenge_json = result.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    remove_files(challenge.code, challenge.tests_code)
    #act
    res = client.get(f'javascript/javascript-challenges/{challenge_id}')
    #assert
    assert res.status_code == 401 
