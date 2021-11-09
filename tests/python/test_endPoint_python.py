from app.python.models import *
from . import client
import json


# testing of one post challenge
def test_post_pythonChallenge(client):
    repair_objective = "make to pass"

    dataChallenge = postFunction(repair_objective, 2)

    response = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallenge)

    assert response.status_code == 200

# testing a single challenge 
def test_get_single_pythonChallenge(client):
    clear_data_base()

    #---- post one challenge to test ---#    
    repair_objectiveParam = "prueba test"

    dataChallengePost = postFunction(repair_objectiveParam,3) 
    client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallengePost)

    result = client.get('http://localhost:5000/python/api/v1/python-challenges/1')
    #---- end post ---#

    #data to be entered in the post test
    dataEnteredPost = {'challenge': {'best_score': 0, 'code': '\ndef median(a,b,c):\n    res = 0\n    if ((a>=b and a<=c) or (a>=c and a<=b)):\n        res = a\n    if ((b>=a and b<=c) or (b>=c and b<=a)):\n        res = b\n    else:\n        res = c\n    return res\n\n', 'complexity': 3, 'repair_objective': 'prueba test', 'tests_code': 'from median import median\n\ndef test_one():\n    a = 1\n    b = 2\n    c = 3\n    res = median(a, b, c)\n    assert res == 2\n\ndef test_two():\n    a = 2\n    b = 1\n    c = 3\n    res = median(a, b, c)\n    assert res == 2\n\ndef test_three():\n    a = 3\n    b = 1\n    c = 2\n    res = median(a, b, c)\n    assert res == 2\n\n'}}

    #data obtained through the get ready for manipulation
    dataChallenge = parseDataTextAJson(result.json)

    #I get each value within the dictionary
    repair_objective = dataChallenge['challenge']['repair_objective']
    best_score       = dataChallenge['challenge']['best_score']
    complexity       = dataChallenge['challenge']['complexity']
    code             = dataChallenge['challenge']['code']

    assert isinstance(complexity,int) == True
    assert len(repair_objective) > 0
    assert len(code) > 0
    assert result.json == dataEnteredPost 
    clear_data_base()

# testing multiple challenges
def test_get_total_pythonChallenge(client):
    clear_data_base()

    #--- start post challenges ---#
    repair_objectiveParamOne = "probando test"
    repair_objectiveParamTwo = "pruebita test"
    repair_objectiveParamThree = "pruebas test"
    
    dataChallengePostOne = postFunction(repair_objectiveParamOne,1)
    dataChallengePostTwo = postFunction(repair_objectiveParamTwo,2)
    dataChallengePostThree = postFunction(repair_objectiveParamThree,3)

    client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallengePostOne)
    client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallengePostTwo)
    client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallengePostThree)
    #--- end post challenges ---#

    responsive = client.get('http://localhost:5000/python/api/v1/python-challenges')
    
    data = parseDataTextAJson(responsive.json)
    
    assert len(data['challenges']) == 3
    clear_data_base()



# -------Section functions ------- #
def parseDataTextAJson(result):
    dataResultText = json.dumps(result)

    dataResultJson = json.loads(dataResultText)

    return dataResultJson

def clear_data_base():
    db.session.query(PythonChallengeModel).delete()

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
# ------- end Section functions ------- #
