from app.python.models import *
from . import client
from app.python.file_utils import read_file
import json

examples_path = 'tests/python/example_programs_test/'
api_url = 'http://localhost:5000/python/api/v1/python-challenges'

# testing of one post challenge
def test_post_pythonChallenge(client):
    repair_objective = "make to pass"
    response = send_post(client, "valid_code_1.py", "valid_test_1.py", repair_objective, 2)

    assert response.status_code == 200

# testing a single challenge 
def test_get_single_pythonChallenge(client):
    #---- post one challenge to test ---#    
    repair_objectiveParam = "prueba test"
    post_info = send_post(client, "valid_code_1.py", "valid_test_1.py", repair_objectiveParam, 3)
    
    challenge_id = parseDataTextAJson(post_info.json)['challenge']['id']
    result = client.get(api_url + '/' + str(challenge_id))
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
    responsive = client.get(api_url)
    initial_challenge_len = len(parseDataTextAJson(responsive.json)['challenges'])
    
    #--- start post challenges ---#
    repair_objectiveParamOne = "probando test"
    send_post(client, "valid_code_1.py", "valid_test_1.py", repair_objectiveParamOne, 1)
    
    repair_objectiveParamTwo = "pruebita test"
    send_post(client, "valid_code_1.py", "valid_test_1.py", repair_objectiveParamTwo, 2)

    #--- end post challenges ---#

    responsive = client.get(api_url)
    
    data = parseDataTextAJson(responsive.json)
    
    assert len(data['challenges']) == initial_challenge_len + 2

def test_post_challenge_invalid_code(client):
    response = send_post(client, "code_not_compile.py", "valid_test_1.py", "Make all tests pass.", 2)

    assert response.status_code == 409
    #get json with the error
    json_response = parseDataTextAJson(response.json)
    assert json_response['Error'] == 'Syntax error at ' + 'code_not_compile.py'

def test_post_challenge_invalid_test(client):
    response = send_post(client, "valid_code_1.py", "test_not_compile.py", "Make all tests pass.", 2)

    assert response.status_code == 409
    #get json with the error
    json_response = parseDataTextAJson(response.json)
    assert json_response['Error'] == 'Syntax error at ' + 'test_not_compile.py'

#post challenge with no errors in tests (so its repaired)
def test_post_invalid_repaired_challenge(client):
    response = send_post(client, "code_repair_2.py", "valid_test_2.py", "Make all tests pass.", 2)

    assert response.status_code == 409
    #get json with the error
    json_response = parseDataTextAJson(response.json)
    assert json_response['Error'] == 'At least one test must fail'


def test_update_simple_fields(client):
    #make a post and save id
    post_info = send_post(client, "valid_code_1.py", "valid_test_1.py", "Make all tests pass.", 1)
    challenge_id = parseDataTextAJson(post_info.json)['challenge']['id']
    #send an update request
    update_request = request_creator(repair_objective="updated", complexity=3)
    response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    update_expected_response = create_expected_response(0, "valid_code_1.py", "3", 'updated', "valid_test_1.py")

    assert response.status_code == 200
    assert response.json == update_expected_response
    #check te same with get
    response = client.get(api_url + '/' + str(challenge_id))
    assert response.json == update_expected_response

def test_update_valid_code(client):
    post_info = send_post(client, "valid_code_1.py", "valid_test_1.py", "Make all tests pass.", 1)

    challenge_id = parseDataTextAJson(post_info.json)['challenge']['id']
    #send an update request
    update_request = request_creator(code_path=examples_path + "valid_code_3.py")
    response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert response.status_code == 200
    #the file has been saved correctly
    assert response.json['challenge']['code'] == read_file(examples_path + 'valid_code_3.py', 'r')

# -------Section functions ------- #
def parseDataTextAJson(result):
    dataResultText = json.dumps(result)

    dataResultJson = json.loads(dataResultText)

    return dataResultJson

def request_creator(**params):
    dataChallenge = {}
    challenge_str = '{ "challenge": { '
    initial_len = len(challenge_str)    #just to know if its been updated in the end
    
    #we check each param's presence and add it to dataChallenge
    if params.get('code_path') is not None:
        dataChallenge['source_code_file'] = open(params.get('code_path'), 'rb')
    if params.get('test_path') is not None:
        dataChallenge['test_suite_file'] = open(params.get('test_path'), 'rb')
    if params.get('code_name') is not None:
        challenge_str += '"source_code_file_name" : "' + params.get('code_name') + '", '
    if params.get('test_name') is not None:
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
    code = read_file(examples_path + code_name, 'r')
    test = read_file(examples_path + test_name, 'r')
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

def send_post(client, code_name, test_name, repair_objective, complexity):
    code_path = examples_path + code_name
    test_path = examples_path + test_name
    
    dataChallengePost = request_creator(code_path=code_path, test_path=test_path, code_name=code_name,
     test_name=test_name, repair_objective=repair_objective, complexity=complexity)

    return client.post(api_url, data=dataChallengePost)
