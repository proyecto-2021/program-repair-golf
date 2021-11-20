from tests.auth import *
from werkzeug.wrappers import response
from app.java.models_java import Challenge_java
from . import client

urlClass = 'example-challenges/java-challenges/Median.java'
urlTest = 'example-challenges/java-challenges/MedianTest.java'
exampleClass = 'tests/java/example_java/Prueba.java'
exampleTest = 'tests/java/example_java/PruebaTest.java'

def delete_db():
	db.session.query(Challenge_java).delete()

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
    
def get_token(client):
	json = {"username": "user", "password":"pass"}
	client.post('/users', json=json)
	r = client.post('/auth', json=json)
	token = r.json['access_token']
	return token

def file_repair(path):
	repair = open(path, 'rb')
	challenge = {
		'source_code_file': repair
	}
	return challenge