from werkzeug.wrappers import response
from app.java.models_java import Challenge_java
from . import client
import json
from app.java.views import *
import os

urlClass = 'example-challenges/java-challenges/Median.java'
urlTest = 'example-challenges/java-challenges/MedianTest.java'
exampleClass = 'tests/java/example_java/Prueba.java'
exampleTest = 'tests/java/example_java/PruebaTest.java'

def delete_db():
	db.session.query(Challenge_java).delete()

# insert a valid challenge and return a status code equal to 200
def test_post_java(client):
	delete_db()
	location = '/java/java-challenges'
	url = 'http://localhost:5000/java/java-challenges'

	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	
	resp = client.post(url, data=data)
	
	assert resp.status_code == 200
	
# insert a valid challenge and get challenge
def test_post_get_all(client):
	delete_db()
	url = 'http://localhost:5000/java/java-challenges'

	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	client.post(url, data=data)
	resp = client.get(url)
	response = json.loads(json.dumps(resp.json))
	a = response['challenges'][0]
	
	assert resp.status_code == 200
	assert len(response['challenges']) == 1
	assert a['repair_objective'] == 'pass'
	assert a['complexity'] == 1
	assert a['id'] != 0

# insert two valid challenges and then get them and compare the results
def test_many_loads(client):
	delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'

	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	data2 = createChallenge('tests/java/example_java/Prueba.java','tests/java/example_java/PruebaTest.java','Prueba','PruebaTest','Pasa','3')
	
	client.post(url, data=data)
	p = client.post(url, data=data2)

	resp = client.get(url)
	response = json.loads(json.dumps(resp.json))
	b = response['challenges']
	
	assert p.status_code == 200
	assert resp.status_code == 200
	assert len(response['challenges']) == 2
	assert b[0]['repair_objective'] == 'pass'
	assert b[1]['repair_objective'] == 'Pasa'

# insert two valid challenges equal, first status code equal 200 and second equal 404
def test_upload_exist(client):
	delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	datab = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	resp = client.post(url, data=data)
	resp2 = client.post(url, data=datab)

	assert resp.status_code == 200
	assert resp2.status_code == 404

# insert java class that does not compile
def test_file_not_compile_class(client):
	delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = createChallenge('tests/java/example_java/Nocompile.java','tests/java/example_java/NocompileTest.java', 'Nocompile', 'NocompileTest', 'nada', '2')
	try:
		resp = client.post(url, data=data)
	except Exception as e:
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"
	assert resp.status_code == 404
	
# insert java test suite that does not compile
def test_file_not_compile_test(client):
	delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = createChallenge('tests/java/example_java/Testfailclass.java','tests/java/example_java/Testfailtest.java', 'Testfailclass', 'Testfailtest', 'cosa', '3')
	try:
		resp = client.post(url, data=data)
	except Exception as e:
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"		
	assert resp.status_code == 404

# insert valid challenge that pass all test
def test_pass_all_test(client):
	delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = createChallenge('tests/java/example_java/Passalltest.java','tests/java/example_java/Passalltesttest.java', 'Passalltest', 'Passalltesttest', 'dale', '5')
	try:
		resp = client.post(url, data=data)
	except Exception as e:
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"
	assert resp.status_code == 404

def test_get_java(client):
	delete_db()
	url = 'http://localhost:5000/java/java-challenges'
	resp = client.get(url)
	a = resp.json
	
	assert resp.status_code == 200
	assert a['challenges'] == []
	
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
#modify a non-existent challenge
def test_PUT_Id_None(client):
	delete_db()
	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')

	#data = createQuery()
	id=5
	url = f'http://localhost:5000/java/java-challenges/{id}'
	p1=client.put(url)
	assert p1.status_code== 404


def test_PUT_Objective_repair(client):
	delete_db()
	
	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	data2 = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'Pasa', '5')
		
	url = 'http://localhost:5000/java/java-challenges'

	r1 = client.post(url, data=data)
	id = r1.json['challenge']['id']
    
	url2 = f'http://localhost:5000/java/java-challenges/{id}'
	
	r2 = client.put(url2, data=data2)
	json2 = r2.json['challenge']
	objetive=json2['repair_objective']
	complexity=json2['complexity']

	fileClass = open(urlClass, 'rb')
	fileTest = open(urlTest, 'rb')
	
	assert r1.status_code == 200
	assert r2.status_code == 200
	assert objetive == "Pasa"
	assert complexity==5

def test_PUT_1(client):

	delete_db()
	db.session.query(Challenge_java).delete()
	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	data2 = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest1', 'pass', '1')
		
	url = 'http://localhost:5000/java/java-challenges'

	r1 = client.post(url, data=data)
	id = r1.json['challenge']['id']
    
	url2 = f'http://localhost:5000/java/java-challenges/{id}'
	
	try:
		r2 = client.put(url2, data=data2)
	except Exception as e:
		assert str(e) == "FileName orCode not Exist"		
	
	assert r1.status_code == 200
	
def test_put_pass_all_test(client):
	delete_db()
	url = 'http://localhost:5000/java/java-challenges'

	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	data2 = createChallenge('tests/java/example_java/Passalltest.java','tests/java/example_java/Passalltesttest.java', 'Passalltest', 'Passalltesttest', 'pass', '1')
	
	#data2 = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest1', 'pass', '1')
	r1 = client.post(url, data=data)
	id = r1.json['challenge']['id']
    
	url2 = f'http://localhost:5000/java/java-challenges/{id}'
	try:
		resp = client.put(url2, data=data2)
	except Exception as e:
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"
	assert resp.status_code == 404
	assert r1.status_code==200

def test_file_not_compile_class(client):
	delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = createChallenge('tests/java/example_java/Nocompile.java','tests/java/example_java/NocompileTest.java', 'Nocompile', 'NocompileTest', 'nada', '2')
	try:
		resp = client.post(url, data=data)
	except Exception as e:
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"
	assert resp.status_code == 404	

# test repair
# upload an file repair valid
def test_valid_repair_file(client):
	#db.session.query(Challenge_java).delete()
	delete_db()
	urladd = 'http://localhost:5000/java/java-challenges'
	id = 1
	urlrepair = f'http://localhost:5000/java/java-challenges/{id}/repair'

	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	resp1= client.post(urladd, data=data)
	form = file_repair('tests/java/example_java/Median.java')
	resp2= client.post(urlrepair, data=form)

	assert resp1.status_code == 200
	assert resp2.status_code == 200

# upload an file repair invalid
def test_no_valid_repair_file(client):
	#db.session.query(Challenge_java).delete()
	delete_db()
	urladd = 'http://localhost:5000/java/java-challenges'
	id = 1
	urlrepair = f'http://localhost:5000/java/java-challenges/{id}/repair'

	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	client.post(urladd, data=data)
	form = file_repair('tests/java/example_java/Prueba.java')
	try:
		resp2= client.post(urlrepair, data=form)
	except Exception as e:
		assert str(e) == 'Error'
	assert resp2.status_code == 404

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

def file_repair(path):
	repair = open(path, 'rb')
	challenge = {
		'source_code_file': repair
	}
	return challenge
