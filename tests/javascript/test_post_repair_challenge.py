import pytest
from . import client, auth 
from . __init__ import createChallenge, remove_files, ChallengeDAO
from . import db
from app.javascript.models_js import JavascriptChallenge


def test_post_repair(client,auth):
    #arrange
    data = createChallenge('median', 'median.test', 'Testing', '1')
    create_challenge = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data)
    challenge_json = create_challenge.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    
    #act
    data_repair = {'source_code_file': open('example-challenges/javascript-challenges/example_pass_0.js','rb')}
    url_repair = f'javascript/javascript-challenges/{challenge_id}/repair'
    resp_repair = client.post(url_repair, data=data_repair, headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)
    #assert
    assert resp_repair.status_code == 200

def test_post_repair_not_pass(client,auth):
    #arrange
    data = createChallenge('median', 'median.test', 'Testing', '1')
    create_challenge = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data)
    challenge_json = create_challenge.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    
    #act
    data_repair = {'source_code_file': open('example-challenges/javascript-challenges/example0.js','rb')}
    url_repair = f'javascript/javascript-challenges/{challenge_id}/repair'
    resp_repair = client.post(url_repair, data=data_repair, headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)
    #assert
    assert resp_repair.status_code == 404

def test_post_repair_not_compile(client,auth):
    #arrange
    data = createChallenge('median', 'median.test', 'Testing', '1')
    create_challenge = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data)
    challenge_json = create_challenge.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    
    #act
    data_repair = {'source_code_file': open('example-challenges/javascript-challenges/median_not_compile.js','rb')}
    url_repair = f'javascript/javascript-challenges/{challenge_id}/repair'
    resp_repair = client.post(url_repair, data=data_repair, headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)
    #assert
    assert resp_repair.status_code == 404

def test_post_repair_not_data(client,auth):
    #arrange
    data = createChallenge('median', 'median.test', 'Testing', '1')
    create_challenge = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data)
    challenge_json = create_challenge.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    
    #act
    data_repair = {'source_code_file': None}
    url_repair = f'javascript/javascript-challenges/{challenge_id}/repair'
    resp_repair = client.post(url_repair, data=data_repair, headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)
    #assert
    assert resp_repair.status_code == 404

def test_post_repair_no_id(client,auth):
    #arrange
    data = createChallenge('median', 'median.test', 'Testing', '1')
    create_challenge = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data)
    challenge_json = create_challenge.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    
    #act
    data_repair = {'source_code_file': None}
    url_repair = f'javascript/javascript-challenges/{challenge_id+1}/repair'
    resp_repair = client.post(url_repair, data=data_repair, headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)
    #assert
    assert resp_repair.status_code == 404

def test_token_not_valid(client, auth):
    #arrange
    data = createChallenge('median', 'median.test', 'Testing', '1')
    create_challenge = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data)
    challenge_json = create_challenge.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    
    #act
    data_repair = {'source_code_file': open('example-challenges/javascript-challenges/example_pass_0.js','rb')}
    auth = 'Token not valid'
    url_repair = f'javascript/javascript-challenges/{challenge_id}/repair'
    resp_repair = client.post(url_repair, data=data_repair, headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)
    #assert
    assert resp_repair.status_code == 401

def test_authentication_required(client,auth):
    #arrange
    data = createChallenge('median', 'median.test', 'Testing', '1')
    create_challenge = client.post('javascript/javascript-challenges', headers={'Authorization': f'JWT {auth}'}, data=data)
    challenge_json = create_challenge.json['Challenge']
    challenge_id = challenge_json['id']
    challenge_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    
    #act
    data_repair = {'source_code_file': open('example-challenges/javascript-challenges/example_pass_0.js','rb')}
    
    url_repair = f'javascript/javascript-challenges/{challenge_id}/repair'
    resp_repair = client.post(url_repair, data=data_repair)
    remove_files(challenge.code, challenge.tests_code)
    #assert
    assert resp_repair.status_code == 401 