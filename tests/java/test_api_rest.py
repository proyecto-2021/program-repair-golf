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

def createQuery():
	fileClass = open(urlClass, 'rb')
	fileTest = open(urlTest, 'rb')
	
	challenge = {
		'source_code_file': fileClass,
		'test_suite_file': fileTest,
		'challenge':'{ \
            "challenge":{\
                "source_code_file_name": "Median",\
                "test_suite_file_name": "MedianTest",\
                "repair_objective": "algo para acomodar",\
                "complexity": "1"\
            }\
        }'
	}
	return challenge

# insert a valid challenge and return a status code equal to 200
def test_post_java(client):
	db.session.query(Challenge_java).delete()
	location = '/java/java-challenges'
	url = 'http://localhost:5000/java/java-challenges'

	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	print(data)
	resp = client.post(url, data=data)
	
	assert resp.status_code == 200
	
# insert a valid challenge and get challenge
def test_post_get_all(client):
	db.session.query(Challenge_java).delete()
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
	db.session.query(Challenge_java).delete()
	url = url = 'http://localhost:5000/java/java-challenges'

	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	data2 = createChallenge('tests/java/example_java/Prueba.java','tests/java/example_java/PruebaTest.java','Prueba','PruebaTest','Pasa','3')
	#data2 = createQuery2(exampleClass, exampleTest)
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
	db.session.query(Challenge_java).delete()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	datab = createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	resp = client.post(url, data=data)
	resp2 = client.post(url, data=datab)

	assert resp.status_code == 200
	assert resp2.status_code == 404

# insert java class that does not compile
def test_file_not_compile_class(client):
	db.session.query(Challenge_java).delete()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = createChallenge('tests/java/example_java/Nocompile.java','tests/java/example_java/NocompileTest.java', 'Nocompile', 'NocompileTest', 'nada', '2')
	try:
		resp = client.post(url, data=data)
	except Exception as e:
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"
	assert resp.status_code == 404
	
# insert java test suite that does not compile
def test_file_not_compile_test(client):
	db.session.query(Challenge_java).delete()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = createChallenge('tests/java/example_java/Testfailclass.java','tests/java/example_java/Testfailtest.java', 'Testfailclass', 'Testfailtest', 'cosa', '3')
	try:
		resp = client.post(url, data=data)
	except Exception as e:
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"		
	assert resp.status_code == 404

# insert valid challenge that pass all test
def test_pass_all_test(client):
	db.session.query(Challenge_java).delete()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = createChallenge('tests/java/example_java/Passalltest.java','tests/java/example_java/Passalltesttest.java', 'Passalltest', 'Passalltesttest', 'dale', '5')
	try:
		resp = client.post(url, data=data)
	except Exception as e:
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"
	assert resp.status_code == 404

def test_get_java(client):
	db.session.query(Challenge_java).delete()
	url = 'http://localhost:5000/java/java-challenges'
	resp = client.get(url)
	a = resp.json
	
	assert resp.status_code == 200
	assert a['challenges'] == []
	
def test_get_Id_after_post(client):
	db.session.query(Challenge_java).delete()
	url = 'http://localhost:5000/java/java-challenges'
	data = createQuery()

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
	db.session.query(Challenge_java).delete()
	id=1
	url2 = f'http://localhost:5000/java/java-challenges/{id}'
	p2 = client.get(url2)
	
	assert p2.status_code == 404


#modify a non-existent challenge
def test_PUT_Id_None(client):
	delete_db
	data = createQuery()
	id=5
	url = f'http://localhost:5000/java/java-challenges/{id}'
	p1=client.put(url)
	
	assert p1.status_code== 404


#modify complexity of an existing challenge 
#modify repair objective of an existing challenge

#modify a non-existent challenge
#modify files ok 
#modify files does not compile 


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
