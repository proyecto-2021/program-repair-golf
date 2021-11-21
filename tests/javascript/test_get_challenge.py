import pytest
from . import client, auth 
from . __init__ import createChallenge
import json

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





