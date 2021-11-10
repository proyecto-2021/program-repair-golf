from app.python.models import *
from . import client
import json


# testing of one post challenge
def test_post_pythonChallenge(client):
    repair_objective = "make to pass"

    dataChallenge = post_function("valid_code.py", "valid_test_imp_valid_code.py", repair_objective, 2)

    response = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallenge)

    assert response.status_code == 200

# testing a single challenge 
def test_get_single_pythonChallenge(client):
    #---- post one challenge to test ---#    
    repair_objectiveParam = "prueba test"

    dataChallengePost = post_function("valid_code.py", "valid_test_imp_valid_code.py", repair_objectiveParam, 3) 
    post_info = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallengePost)
    
    challenge_id = parseDataTextAJson(post_info.json)['challenge']['id']
    result = client.get('http://localhost:5000/python/api/v1/python-challenges/' + str(challenge_id))
    #---- end post ---#

    #data to be entered in the post test
    post_expected_response = {
        'challenge': {
            'best_score': 0, 
            'code': '\ndef median(a,b,c):\n    res = 0\n    if ((a>=b and a<=c) or (a>=c and a<=b)):\n        res = a\n    if ((b>=a and b<=c) or (b>=c and b<=a)):\n        res = b\n    else:\n        res = c\n    return res\n\n', 
            'complexity': 3, 
            'repair_objective': 'prueba test', 
            'tests_code': 'from valid_code import median\n\ndef test_one():\n    a = 1\n    b = 2\n    c = 3\n    res = median(a, b, c)\n    assert res == 2\n\ndef test_two():\n    a = 2\n    b = 1\n    c = 3\n    res = median(a, b, c)\n    assert res == 2\n\ndef test_three():\n    a = 3\n    b = 1\n    c = 2\n    res = median(a, b, c)\n    assert res == 2\n\n'
        }
    }

    #data obtained through the get ready for manipulation
    dataChallenge = parseDataTextAJson(result.json)

    #I get each value within the dictionary
    repair_objective = dataChallenge['challenge']['repair_objective']
    complexity       = dataChallenge['challenge']['complexity']
    code             = dataChallenge['challenge']['code']

    assert isinstance(complexity,int) == True
    assert len(repair_objective) > 0
    assert len(code) > 0
    assert result.json == post_expected_response

# testing multiple challenges
def test_get_total_pythonChallenge(client):
    #get challenge count before test
    responsive = client.get('http://localhost:5000/python/api/v1/python-challenges')
    initial_challenge_len = len(parseDataTextAJson(responsive.json)['challenges'])
    
    #--- start post challenges ---#
    repair_objectiveParamOne = "probando test"
    repair_objectiveParamTwo = "pruebita test"
    repair_objectiveParamThree = "pruebas test"
    
    dataChallengePostOne = post_function("valid_code.py", "valid_test_imp_valid_code.py", repair_objectiveParamOne, 1)
    dataChallengePostTwo = post_function("valid_code.py", "valid_test_imp_valid_code.py", repair_objectiveParamTwo, 2)
    dataChallengePostThree = post_function("valid_code.py", "valid_test_imp_valid_code.py", repair_objectiveParamThree, 3)

    client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallengePostOne)
    client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallengePostTwo)
    client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallengePostThree)
    #--- end post challenges ---#

    responsive = client.get('http://localhost:5000/python/api/v1/python-challenges')
    
    data = parseDataTextAJson(responsive.json)
    
    assert len(data['challenges']) == initial_challenge_len + 3


def test_post_challenge_invalid_code(client):
    code_filename = "code_not_compile.py"
    dataChallenge = post_function(code_filename, "valid_test_imp_valid_code.py", "Make all tests pass.", 2)

    response = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallenge)

    assert response.status_code == 409
    #get json with the error
    json_response = parseDataTextAJson(response.json)
    assert json_response['Error'] == 'Syntax error at ' + code_filename

# -------Section functions ------- #
def parseDataTextAJson(result):
    dataResultText = json.dumps(result)

    dataResultJson = json.loads(dataResultText)

    return dataResultJson

def clear_data_base():
    db.session.query(PythonChallengeModel).delete()

def post_function(code_name, test_name, repair_objective, complexity):
    
    complexityString = str(complexity)

    source_code_fileTemp = open('tests/python/example_programs_test/' + code_name, 'rb')
    test_suite_fileTemp = open('tests/python/example_programs_test/' + test_name, 'rb')
    dataChallenge = {
        'source_code_file' : source_code_fileTemp,
        'test_suite_file' : test_suite_fileTemp,
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "code_name_variable", \
                "test_suite_file_name" : "test_name_variable", \
                "repair_objective" : "repair_variable" , \
                "complexity" : "complexity_variable" \
            } \
        }'
    } 
    dataChallenge['challenge'] = dataChallenge['challenge'].replace('code_name_variable',code_name)
    dataChallenge['challenge'] = dataChallenge['challenge'].replace('test_name_variable',test_name)
    dataChallenge['challenge'] = dataChallenge['challenge'].replace('repair_variable',repair_objective)
    dataChallenge['challenge'] = dataChallenge['challenge'].replace('complexity_variable',complexityString)

    return dataChallenge     
# ------- end Section functions ------- #
