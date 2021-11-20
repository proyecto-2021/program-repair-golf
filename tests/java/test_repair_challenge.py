from . import client
import json
from app.java.views import *
from tests.auth import *
from tests.java import data_for_tests

# test repair
# upload an file repair valid
def test_valid_repair_file(client):
	data_for_tests.delete_db()
	urladd = 'http://localhost:5000/java/java-challenges'
	id = 1
	urlrepair = f'http://localhost:5000/java/java-challenges/{id}/repair'

	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	token = data_for_tests.get_token(client)
	
	resp1= client.post(urladd, headers={'Authorization': f'JWT {token}'}, data=data)
	form = data_for_tests.file_repair('tests/java/example_java/Median.java')
	resp2= client.post(urlrepair, headers={'Authorization': f'JWT {token}'}, data=form)

	assert resp1.status_code == 200
	assert resp2.status_code == 200

# upload an file repair invalid
def test_no_valid_repair_file(client):
	data_for_tests.delete_db()
	urladd = 'http://localhost:5000/java/java-challenges'
	id = 1
	urlrepair = f'http://localhost:5000/java/java-challenges/{id}/repair'

	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	token = data_for_tests.get_token(client)
	client.post(urladd, headers={'Authorization': f'JWT {token}'}, data=data)
	form = data_for_tests.file_repair('tests/java/example_java/Prueba.java')
	try:
		resp2 = client.post(urlrepair, headers={'Authorization': f'JWT {token}'}, data=form)
	except Exception as e:
		assert str(e) == 'Error'
	assert resp2.status_code == 404

def test_repair_invalid_token(client):
	data_for_tests.delete_db()
	urladd = 'http://localhost:5000/java/java-challenges'
	id = 1
	urlrepair = f'http://localhost:5000/java/java-challenges/{id}/repair'

	data = data_for_tests.createChallenge('example-challenges/java-challenges/Median.java','example-challenges/java-challenges/MedianTest.java','Median','MedianTest', 'pass', '1')
	token = data_for_tests.get_token(client)
	client.post(urladd, headers={'Authorization': f'JWT {token}'}, data=data)
	form = data_for_tests.file_repair('tests/java/example_java/Prueba.java')
	new_token = 'cualquierTokenParaElRepair'
	try:
		resp2 = client.post(urlrepair, headers={'Authorization': f'JWT {new_token}'}, data=form)
	except Exception as e:
		assert str(e) == 'Error'
	assert resp2.status_code == 401
