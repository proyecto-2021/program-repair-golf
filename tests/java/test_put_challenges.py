from werkzeug.wrappers import response
from app.java.models_java import Challenge_java
from . import client
import json
from app.java.views import *
import os
from tests.auth import *
from tests.java import data_for_tests


#modify a non-existent challenge
def test_PUT_Id_None(client):
	#arrange
	data_for_tests.delete_db
	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	id=5
	url = f'http://localhost:5000/java/java-challenges/{id}'
	token=data_for_tests.get_token(client)

	#act
	p1=client.put(url, headers={'Authorization': f'JWT {token}'})
	
	#assert
	assert p1.status_code== 404


def test_PUT_parameters_tokenOK(client):
	#arrange
	data_for_tests.delete_db()
	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	data2 = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'Pasa', '5')
	token=data_for_tests.get_token(client)
	url = 'http://localhost:5000/java/java-challenges'
	r1 = client.post(url,headers={'Authorization': f'JWT {token}'}, data=data)
	id = r1.json['challenge']['id']
	url2 = f'http://localhost:5000/java/java-challenges/{id}'
	
	#act
	r2 = client.put(url2,headers={'Authorization': f'JWT {token}'}, data=data2)
	json2 = r2.json['challenge']
	objetive=json2['repair_objective']
	complexity=json2['complexity']

	#fileClass = open(data_for_tests.urlClass, 'rb')
	#fileTest = open(data_for_tests.urlTest, 'rb')
	
	#assert
	assert r1.status_code == 200
	assert r2.status_code == 200
	assert objetive == "Pasa"
	assert complexity==5

def test_PUT_parameters_Error_token(client):
	#arrange
	data_for_tests.delete_db()
	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	data2 = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'Pasa', '5')
	token=data_for_tests.get_token(client)
	token1="dggfgfhfghgfjfghdr4557ythgh"
	url = 'http://localhost:5000/java/java-challenges'
	r1 = client.post(url,headers={'Authorization': f'JWT {token}'}, data=data)
	id = r1.json['challenge']['id']	
	url2 = f'http://localhost:5000/java/java-challenges/{id}'
	#act
	r2 = client.put(url2,headers={'Authorization': f'JWT {token1}'},data=data2)

	#assert
	assert r1.status_code == 200
	assert r2.status_code == 401

def test_PUT_fails_parameters(client):
	#arrange
	data_for_tests.delete_db()
	db.session.query(Challenge_java).delete()
	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	data2 = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest1', 'pass', '1')
	
	token=data_for_tests.get_token(client)	
	url = 'http://localhost:5000/java/java-challenges'
	r1 = client.post(url,headers={'Authorization': f'JWT {token}'}, data=data)
	id = r1.json['challenge']['id']
	url2 = f'http://localhost:5000/java/java-challenges/{id}'

	#act
	try:
		r2 = client.put(url2, headers={'Authorization': f'JWT {token}'}, data=data2)
	except Exception as e:
		assert str(e) == "FileName orCode not Exist"		
	#assert
	assert r1.status_code == 200
	
def test_PUT_pass_all_test(client):
	#arrange
	data_for_tests.delete_db()
	url = 'http://localhost:5000/java/java-challenges'
	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	data2 = data_for_tests.createChallenge('tests/java/example_java/Passalltest.java','tests/java/example_java/Passalltesttest.java', 'Passalltest', 'Passalltesttest', 'pass', '1')
	token=data_for_tests.get_token(client)	
	r1 = client.post(url, headers={'Authorization': f'JWT {token}'},data=data)
	id = r1.json['challenge']['id']
	url2 = f'http://localhost:5000/java/java-challenges/{id}'
	#act
	try:
		resp = client.put(url2,headers={'Authorization': f'JWT {token}'}, data=data2)
	except Exception as e:
	#assert
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"
	assert resp.status_code == 404
	assert r1.status_code==200

def test_file_PUT_not_compile_class(client):
	#arrange
	data_for_tests.delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	data2 = data_for_tests.createChallenge('tests/java/example_java/Nocompile.java','tests/java/example_java/NocompileTest.java', 'Nocompile', 'NocompileTest', 'pass', '1')
	token=data_for_tests.get_token(client)	
	r1 = client.post(url,headers={'Authorization': f'JWT {token}'}, data=data)
	id = r1.json['challenge']['id']
	url2 = f'http://localhost:5000/java/java-challenges/{id}'
	#act
	try:
		resp = client.put(url,headers={'Authorization': f'JWT {token}'}, data=data2)
	except Exception as e:
	#assert
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"


# update java test suite that does not compile
def PUT_test_file_not_compile_test(client):
	#arrange
	data_for_tests.delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	data2 = data_for_tests.createChallenge('tests/java/example_java/Testfailclass.java','tests/java/example_java/Testfailtest.java', 'Testfailclass', 'Testfailtest', 'pass', '1')
	token=data_for_tests.get_token(client)	
	r1 = client.post(url,headers={'Authorization': f'JWT {token}'}, data=data)
	id = r1.json['challenge']['id']
    
	url2 = f'http://localhost:5000/java/java-challenges/{id}'
	#act
	try:
		resp = client.put(url,headers={'Authorization': f'JWT {token}'}, data=data2)
	except Exception as e:
	#assert
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"		
	assert resp.status_code == 404	