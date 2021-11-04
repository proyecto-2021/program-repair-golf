from app.python.models import *
from . import client
import json



def test_post_pythonChallenge(client):
    
    source_code_fileTemp = open('example-challenges/python-challenges/median.py','rb')
    test_suite_fileTemp = open('example-challenges/python-challenges/test_median.py','rb')
    dataChallenge = {
        'source_code_file' : source_code_fileTemp,
        'test_suite_file' : test_suite_fileTemp,
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "median.py", \
                "test_suite_file_name" : "test_median.py", \
                "repair_objective" : "make all test pass", \
                "complexity" : "1" \
            } \
        }'
    }    
    

    response = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallenge)
    assert response.status_code == 200

def test_get_total_pythonChallenge(client):
    result = client.get('http://localhost:5000/python/api/v1/python-challenges')
    
    #data to be entered in the post test
    dataEnteredPost = {'challenges': [{'best_score': 0, 'code': '\ndef median(a,b,c):\n    res = 0\n    if ((a>=b and a<=c) or (a>=c and a<=b)):\n        res = a\n    if ((b>=a and b<=c) or (b>=c and b<=a)):\n        res = b\n    else:\n        res = c\n    return res\n\n', 'complexity': 1, 'id': 1, 'repair_objective': 'make all test pass'}]}

    #data obtained through the get ready for manipulation
    dataChallenge = parseDataTextAJson(result.json)

    #I get each value within the dictionary
    repair_objective = dataChallenge['challenges'][0]['repair_objective']
    best_score       = dataChallenge['challenges'][0]['best_score']
    complexity       = dataChallenge['challenges'][0]['complexity']
    code             = dataChallenge['challenges'][0]['code']


    assert isinstance(complexity,int) == True
    assert len(repair_objective) > 0
    assert len(code) > 0
    assert result.json == dataEnteredPost 
    





def parseDataTextAJson(data):
    dataResultText = json.dumps(data)

    dataResultJson = json.loads(dataResultText)

    return dataResultJson

