from app.python.models import *
from . import client
import json



def test_post_pythonChallenge(client):
    repair_objective = "make to pass"

    dataChallenge = postFunction(repair_objective, 2)

    response = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallenge)

    assert response.status_code == 200



def test_get_single_pythonChallenge(client):
    result = client.get('http://localhost:5000/python/api/v1/python-challenges/1')
    
    #data to be entered in the post test
    dataEnteredPost = {'Challenge': {'best_score': 0, 'code': '\ndef median(a,b,c):\n    res = 0\n    if ((a>=b and a<=c) or (a>=c and a<=b)):\n        res = a\n    if ((b>=a and b<=c) or (b>=c and b<=a)):\n        res = b\n    else:\n        res = c\n    return res\n\n', 'complexity': 2, 'repair_objective': 'make to pass', 'tests_code': 'from median import median\n\ndef test_one():\n    a = 1\n    b = 2\n    c = 3\n    res = median(a, b, c)\n    assert res == 2\n\ndef test_two():\n    a = 2\n    b = 1\n    c = 3\n    res = median(a, b, c)\n    assert res == 2\n\ndef test_three():\n    a = 3\n    b = 1\n    c = 2\n    res = median(a, b, c)\n    assert res == 2\n\n'}}

    #data obtained through the get ready for manipulation
    dataChallenge = parseDataTextAJson(result.json)

    #I get each value within the dictionary
    repair_objective = dataChallenge['Challenge']['repair_objective']
    best_score       = dataChallenge['Challenge']['best_score']
    complexity       = dataChallenge['Challenge']['complexity']
    code             = dataChallenge['Challenge']['code']

    assert isinstance(complexity,int) == True
    assert len(repair_objective) > 0
    assert len(code) > 0
    assert result.json == dataEnteredPost 
    



# -------Section functions ------- #
def parseDataTextAJson(result):
    dataResultText = json.dumps(result)

    dataResultJson = json.loads(dataResultText)

    return dataResultJson

def postFunction(repair_objectiveParam,complexityParam):
    
    complexityString = str(complexityParam)

    source_code_fileTemp = open('example-challenges/python-challenges/median.py','rb')
    test_suite_fileTemp = open('example-challenges/python-challenges/test_median.py','rb')
    dataChallenge = {
        'source_code_file' : source_code_fileTemp,
        'test_suite_file' : test_suite_fileTemp,
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "median.py", \
                "test_suite_file_name" : "test_median.py", \
                "repair_objective" : "repair_variable" , \
                "complexity" : "complexity_variable" \
            } \
        }'
    } 
    replace_text = dataChallenge['challenge'].replace('repair_variable',repair_objectiveParam)
    dataChallenge['challenge'] = replace_text
    replace_text2 = dataChallenge['challenge'].replace('complexity_variable',complexityString)
    dataChallenge['challenge'] = replace_text2

    return dataChallenge     
