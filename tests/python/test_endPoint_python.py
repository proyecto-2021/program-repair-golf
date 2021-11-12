from app.python.models import *
from . import client
from app.python.file_utils import read_file
import json


# testing of one post challenge
def test_post_pythonChallenge(client):
    repair_objective = "make to pass"

    dataChallenge = request_creator(code_name="valid_code_1.py", test_name="valid_test_1.py", repair_objective=repair_objective, complexity=2)

    response = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallenge)

    assert response.status_code == 200

# testing a single challenge 
def test_get_single_pythonChallenge(client):
    #---- post one challenge to test ---#    
    repair_objectiveParam = "prueba test"

    dataChallengePost = request_creator(code_name="valid_code_1.py", test_name="valid_test_1.py", repair_objective=repair_objectiveParam, complexity=3)
    post_info = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallengePost)
    
    challenge_id = parseDataTextAJson(post_info.json)['challenge']['id']
    result = client.get('http://localhost:5000/python/api/v1/python-challenges/' + str(challenge_id))
    #---- end post ---#

    #data to be entered in the post test
    post_expected_response = create_expected_response(0, "valid_code_1.py", "3", 'prueba test', "valid_test_1.py")

    #data obtained through the get ready for manipulation
    dataChallenge = parseDataTextAJson(result.json)

    #I get each value within the dictionary
    repair_objective = dataChallenge['challenge']['repair_objective']
    code             = dataChallenge['challenge']['code']

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
    
    dataChallengePostOne = request_creator(code_name="valid_code_1.py", test_name="valid_test_1.py", repair_objective=repair_objectiveParamOne, complexity=1)
    dataChallengePostTwo = request_creator(code_name="valid_code_1.py", test_name="valid_test_1.py", repair_objective=repair_objectiveParamTwo, complexity=2)

    client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallengePostOne)
    client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallengePostTwo)
    #--- end post challenges ---#

    responsive = client.get('http://localhost:5000/python/api/v1/python-challenges')
    
    data = parseDataTextAJson(responsive.json)
    
    assert len(data['challenges']) == initial_challenge_len + 2

def test_post_challenge_invalid_code(client):
    code_filename = "code_not_compile.py"
    dataChallenge = request_creator(code_name=code_filename, test_name="valid_test_1.py", repair_objective="Make all tests pass.", complexity=2)

    response = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallenge)

    assert response.status_code == 409
    #get json with the error
    json_response = parseDataTextAJson(response.json)
    assert json_response['Error'] == 'Syntax error at ' + code_filename

def test_post_challenge_invalid_test(client):
    test_filename = "test_not_compile.py"
    dataChallenge = request_creator(code_name="valid_code_1.py", test_name=test_filename, repair_objective="Make all tests pass.", complexity=2)

    response = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallenge)

    assert response.status_code == 409
    #get json with the error
    json_response = parseDataTextAJson(response.json)
    assert json_response['Error'] == 'Syntax error at ' + test_filename

#post challenge with no errors in tests (so its repaired)
def test_post_invalid_repaired_challenge(client):
    dataChallenge = request_creator(code_name="code_repair_2.py", test_name="valid_test_2.py", repair_objective="Make all tests pass.", complexity=2)

    response = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallenge)

    assert response.status_code == 409
    #get json with the error
    json_response = parseDataTextAJson(response.json)
    assert json_response['Error'] == 'At least one test must fail'


def test_update_simple_fields(client):
    #make a post and save id
    dataChallengePost = request_creator(code_name="valid_code_1.py", test_name="valid_test_1.py", repair_objective="Make all tests pass.", complexity=1)
    post_info = client.post('http://localhost:5000/python/api/v1/python-challenges', data=dataChallengePost)
    
    challenge_id = parseDataTextAJson(post_info.json)['challenge']['id']
    #send an update request
    updateRequest = request_creator(repair_objective="updated", complexity=3)
    response = client.put('http://localhost:5000/python/api/v1/python-challenges/' + str(challenge_id), data=updateRequest)

    update_expected_response = create_expected_response(0, "valid_code_1.py", "3", 'updated', "valid_test_1.py")

    assert response.status_code == 200
    assert response.json == update_expected_response
    #check te same with get
    response = client.get('http://localhost:5000/python/api/v1/python-challenges/' + str(challenge_id))
    assert response.json == update_expected_response

# -------Section functions ------- #
def parseDataTextAJson(result):
    dataResultText = json.dumps(result)

    dataResultJson = json.loads(dataResultText)

    return dataResultJson

def request_creator(**params):
    #we check each param's presence and add it to dataChallenge
    dataChallenge = {}
    challenge_str = '{ "challenge": { '
    initial_len = len(challenge_str)    #just to know if its been updated in the end
    if params.get('code_name') is not None:
        source_code_fileTemp = open('tests/python/example_programs_test/' + params.get('code_name'), 'rb')
        dataChallenge['source_code_file'] = source_code_fileTemp
        challenge_str += '"source_code_file_name" : "' + params.get('code_name') + '", '
    if params.get('test_name') is not None:
        test_suite_fileTemp = open('tests/python/example_programs_test/' + params.get('test_name'), 'rb')
        dataChallenge['test_suite_file'] = test_suite_fileTemp
        challenge_str += '"test_suite_file_name" : "' + params.get('test_name') + '", '
    if params.get('repair_objective') is not None:
        challenge_str += '"repair_objective" : "' + params.get('repair_objective') + '" , '
    if params.get('complexity') is not None:
        challenge_str += '"complexity" : "' + str(params.get('complexity')) + '" '
    challenge_str += '} }'
    #checking if some param has been passed
    if len(challenge_str) > initial_len + len('} }'):
        dataChallenge['challenge'] = challenge_str

    return dataChallenge     
# ------- end Section functions ------- #

def create_expected_response(best_score, code_name, complexity, repair_objective, test_name):
    code = read_file('tests/python/example_programs_test/' + code_name, 'r')
    test = read_file('tests/python/example_programs_test/' + test_name, 'r')
    expected_response = {
        'challenge': {
            'best_score': best_score,
            'code': code,
            'complexity': complexity,
            'repair_objective': repair_objective,
            'tests_code': test
        }
    }
    return expected_response