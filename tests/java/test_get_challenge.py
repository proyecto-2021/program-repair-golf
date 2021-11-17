from werkzeug.wrappers import response
from app.java.models_java import Challenge_java
from . import client
import json
from app.java.views import *
import os
from tests.auth import *
from tests.java import data_for_tests

def test_get_Id_after_post(client):
	db.session.query(Challenge_java).delete()
    #arrange
	url = 'http://localhost:5000/java/java-challenges'
	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	token=data_for_tests.get_token(client)

	p = client.post(url,headers={'Authorization': f'JWT {token}'}, data=data)
	json = p.json['challenge']
	id = json['id']

	url2 = f'http://localhost:5000/java/java-challenges/{id}'
    #act
	p2 = client.get(url2, headers={'Authorization': f'JWT {token}'})
	json2 = p2.json['challenge']
	id2=json2['id']
    #assert
	assert p.status_code == 200
	assert p2.status_code == 200
	assert id == id2

def test_get_Id_novalido(client):
    db.session.query(Challenge_java).delete()
    #arr
    id='hola' 
    url2 = f'http://localhost:5000/java/java-challenges/{id}'
    token=data_for_tests.get_token(client)
    #act
    p2 = client.get(url2, headers={'Authorization': f'JWT {token}'})
	#assert
    assert p2.status_code == 404

def test_get_Id_noesxite(client):
    db.session.query(Challenge_java).delete()
    #arr
    id=1
    url2 = f'http://localhost:5000/java/java-challenges/{id}'
    token=data_for_tests.get_token(client)
    #act
    p2 = client.get(url2, headers={'Authorization': f'JWT {token}'})
	#assert
    assert p2.status_code == 404

def test_get_java(client):
	data_for_tests.delete_db()
	#arr
	url = 'http://localhost:5000/java/java-challenges'
	token = data_for_tests.get_token(client)
	#act
	resp = client.get(url, headers={'Authorization': f'JWT {token}'})
	a = resp.json
	#assert
	assert resp.status_code == 200
	assert a['challenges'] == []

def test_get_java_not_token(client):
	data_for_tests.delete_db()
	#arr
	url = 'http://localhost:5000/java/java-challenges'
	token = "ghghghhgg"
	#act
	resp = client.get(url, headers={'Authorization': f'JWT {token}'})
	a = resp.json
	#assert
	assert resp.status_code == 401
	

