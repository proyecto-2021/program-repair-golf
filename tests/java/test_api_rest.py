from werkzeug.wrappers import response
from app.java.models_java import Challenge_java
from . import client
import json
from app.java.views import *
import os
from tests.auth import *

urlClass = 'example-challenges/java-challenges/Median.java'
urlTest = 'example-challenges/java-challenges/MedianTest.java'
exampleClass = 'tests/java/example_java/Prueba.java'
exampleTest = 'tests/java/example_java/PruebaTest.java'

def delete_db():
	db.session.query(Challenge_java).delete()

def test_get_Id_after_post(client):
	db.session.query(Challenge_java).delete()
	url = 'http://localhost:5000/java/java-challenges'
	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')


	p = client.post(url, data=data)
	json = p.json['challenge']
	id = json['id']

	url2 = f'http://localhost:5000/java/java-challenges/{id}'
	p2 = client.get(url2)
	json2 = p2.json['challenge']
	id2=json2['id']

	assert p.status_code == 200
	assert p2.status_code == 200
	assert id == id2

def test_get_Id_noesxite(client):
	delete_db()
	id=1
	url2 = f'http://localhost:5000/java/java-challenges/{id}'
	p2 = client.get(url2)
	
	assert p2.status_code == 404

def test_get_Id_novalido(client):
	db.session.query(Challenge_java).delete()
	id='hola' 
	url2 = f'http://localhost:5000/java/java-challenges/{id}'
	p2 = client.get(url2)
	
	#assert p2.status_code == 404
	assert p2.status_code == 404

def createChallenge(url_class, url_test, name_class, name_test, objective, complexity):
	fileClass = open(url_class, 'rb')
	fileTest = open(url_test, 'rb')
	
	challenge = {
		'source_code_file': fileClass,
		'test_suite_file': fileTest,
		'challenge':'{ \
            "challenge":{\
                "source_code_file_name": "Median",\
                "test_suite_file_name": "MedianTest",\
                "repair_objective": "algo",\
                "complexity": "w"\
            }\
        }'
	}
	challenge['challenge'] = challenge['challenge'].replace('Median', name_class)
	challenge['challenge'] = challenge['challenge'].replace('MedianTest', name_test)
	challenge['challenge'] = challenge['challenge'].replace('algo', objective)
	challenge['challenge'] = challenge['challenge'].replace('w', complexity)
	
	return challenge

def createChallenge1(url_class, url_test, name_class, name_test, objective, complexity,best_score):
	fileClass = open(url_class, 'rb')
	fileTest = open(url_test, 'rb')
	
	challenge = {
		'source_code_file': fileClass,
		'test_suite_file': fileTest,
		'challenge':'{ \
            "challenge":{\
                "source_code_file_name": "Median",\
                "test_suite_file_name": "MedianTest",\
                "repair_objective": "algo",\
                "complexity": "w"\
				"best_score": "500"\
            }\
        }'
	}
	challenge['challenge'] = challenge['challenge'].replace('Median', name_class)
	challenge['challenge'] = challenge['challenge'].replace('MedianTest', name_test)
	challenge['challenge'] = challenge['challenge'].replace('algo', objective)
	challenge['challenge'] = challenge['challenge'].replace('w', complexity)
	challenge['challenge'] = challenge['challenge'].replace('w', best_score)
	
	return challenge

def get_token(client):
	json = {"username": "user", "password":"pass"}
	client.post('/users', json=json)
	r = client.post('/auth', json=json)
	token = r.json['access_token']
	return token