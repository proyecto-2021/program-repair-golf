import pytest
from . import client, auth 
from . __init__ import createChallenge, post_generator,remove_files, ChallengeDAO
from . import db
from app.javascript.models_js import JavascriptChallenge

#Test de hacer un get luego de hacer un post

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

def test_get_after_post(client, auth, post_generator):
    # arrange
    orig_json = post_generator['Challenge'].copy()
    challenge_id = orig_json['id']
    orig_json.pop('id')
    challenge = ChallengeDAO.get_challenge(challenge_id)
    
    # act
    r = client.get(f'javascript/javascript-challenges/{challenge_id}', headers={'Authorization': f'JWT {auth}'})
    remove_files(challenge.code, challenge.tests_code)

    # assert
    assert r.status_code == 200