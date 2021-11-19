from . import client
from app.java.views import *
from tests.auth import *
from tests.java import data_for_tests
import json

# insert a valid challenge and return a status code equal to 200
def test_post_java(client):
	data_for_tests.delete_db()
	url = 'http://localhost:5000/java/java-challenges'
	token = data_for_tests.get_token(client)
	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	resp = client.post(url, headers={'Authorization': f'JWT {token}'}, data=data)
	
	assert resp.status_code == 200
	
def test_post_java_token_invalid(client):
	data_for_tests.delete_db()
	url = '/java/java-challenges'
	token = 'cualquierCosaDeToken'
	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	resp = client.post(url, headers={'Authorization': f'JWT {token}'}, data=data)

	assert resp.status_code == 401

# insert a valid challenge and get challenge
def test_post_get_all(client):
	data_for_tests.delete_db()
	url = 'http://localhost:5000/java/java-challenges'

	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	token = data_for_tests.get_token(client)
	client.post(url, headers={'Authorization': f'JWT {token}'}, data=data)
	resp = client.get(url, headers={'Authorization': f'JWT {token}'})
	response = json.loads(json.dumps(resp.json))
	a = response['challenges'][0]
	
	assert resp.status_code == 200
	assert len(response['challenges']) == 1
	assert a['repair_objective'] == 'pass'
	assert a['complexity'] == 1
	assert a['id'] != 0

def test_post_complexity_invalid(client):
	data_for_tests.delete_db()
	url = 'http://localhost:5000/java/java-challenges'
	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '7')
	token = data_for_tests.get_token(client)
	try:
		client.post(url, headers={'Authorization': f'JWT {token}'}, data=data)
	except Exception as e:
		assert str(e) == "The complexity is greater than 5, it must be less than equal to 5"

# insert two valid challenges and then get them and compare the results
def test_many_loads(client):
	data_for_tests.delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'

	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	data2 = data_for_tests.createChallenge('tests/java/example_java/Prueba.java','tests/java/example_java/PruebaTest.java','Prueba','PruebaTest','Pasa','3')
	token = data_for_tests.get_token(client)
	client.post(url, headers={'Authorization': f'JWT {token}'}, data=data)
	p = client.post(url, headers={'Authorization': f'JWT {token}'}, data=data2)

	resp = client.get(url, headers={'Authorization': f'JWT {token}'})
	response = json.loads(json.dumps(resp.json))
	b = response['challenges']
	
	assert p.status_code == 200
	assert resp.status_code == 200
	assert len(response['challenges']) == 2
	assert b[0]['repair_objective'] == 'pass'
	assert b[1]['repair_objective'] == 'Pasa'

# insert two valid challenges equal, first status code equal 200 and second equal 404
def test_upload_exist(client):
	data_for_tests.delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	datab = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	token = data_for_tests.get_token(client)
	resp = client.post(url, headers={'Authorization': f'JWT {token}'}, data=data)
	resp2 = client.post(url, headers={'Authorization': f'JWT {token}'}, data=datab)

	assert resp.status_code == 200
	assert resp2.status_code == 404

# insert java class that does not compile
def test_file_not_compile_class(client):
	data_for_tests.delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = data_for_tests.createChallenge('tests/java/example_java/Nocompile.java','tests/java/example_java/NocompileTest.java', 'Nocompile', 'NocompileTest', 'nada', '2')
	token = data_for_tests.get_token(client)
	try:
		resp = client.post(url, headers={'Authorization': f'JWT {token}'}, data=data)
	except Exception as e:
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"
	assert resp.status_code == 404
	
# insert java test suite that does not compile
def test_file_not_compile_test(client):
	data_for_tests.delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = data_for_tests.createChallenge('tests/java/example_java/Testfailclass.java','tests/java/example_java/Testfailtest.java', 'Testfailclass', 'Testfailtest', 'cosa', '3')
	token = data_for_tests.get_token(client)
	try:
		resp = client.post(url, headers={'Authorization': f'JWT {token}'}, data=data)
	except Exception as e:
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"		
	assert resp.status_code == 404

# insert valid challenge that pass all test
def test_pass_all_test(client):
	data_for_tests.delete_db()
	url = url = 'http://localhost:5000/java/java-challenges'
	data = data_for_tests.createChallenge('tests/java/example_java/Passalltest.java','tests/java/example_java/Passalltesttest.java', 'Passalltest', 'Passalltesttest', 'dale', '5')
	token = data_for_tests.get_token(client)
	try:
		resp = client.post(url, headers={'Authorization': f'JWT {token}'}, data=data)
	except Exception as e:
		assert str(e) == "Algun archivo no compila o pasa todos los test, debe fallar algun test para cargar"
	assert resp.status_code == 404