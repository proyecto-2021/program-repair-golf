from app.python.models import *
from . import client
import json


def test_post_pythonChallenge(client):
    # route = 'http://localhost:5000/python/api/v1/python-challenges'
    
    source_code_fileTemp = open('example-challenges/python-challenges/median.py','rb')
    test_suite_fileTemp = open('example-challenges/python-challenges/test_median.py','rb')
    files = {'source_code_file': source_code_fileTemp, 'test_suite_file': test_suite_fileTemp}
    dataChallenge = {
        'challenge': {
            "challenge": {
                "source_code_file_name" : "median.py",
                "test_suite_file_name" : "test_median.py",
                "repair_objective" : "Make all tests pass.",
                "complexity" : "1" 
            }
        }
    }    
    

    response = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallenge)
    print(response.json)

    assert response.status_code == 200
