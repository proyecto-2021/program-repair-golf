from . import client, jwt_token
from .atest_utils import *
import json


def test_get_challenge_not_found(client, jwt_token):
    
    invalid_id = 1000000000000000
    result = client.get(api_url + '/' + str(invalid_id), headers={'Authorization': f'JWT {jwt_token}'})

    assert result.status_code == 409
    assert result.json['Error'] == "Challenge not found"

# testing a single challenge 
def test_get_single_pythonChallenge(client, jwt_token):
    #---- post one challenge to test ---#    
    repair_objectiveParam = "prueba test"
    post_info = send_post(client, jwt_token, "valid_code_5.py", "valid_atest_5.py", repair_objectiveParam, "3")
    
    challenge_id = post_info.json['challenge']['id']
    result = client.get(api_url + '/' + str(challenge_id), headers={'Authorization': f'JWT {jwt_token}'})
    #---- end post ---#

    #data to be entered in the post test
    get_expected_response = create_expected_response(0, "valid_code_1.py", "3", 'prueba test', "valid_atest_5.py")

    #data obtained through the get ready for manipulation
    dataChallenge = result.json

    #I get each value within the dictionary
    repair_objective = dataChallenge['challenge']['repair_objective']
    code             = dataChallenge['challenge']['code']

    assert len(repair_objective) > 0
    assert len(code) > 0
    assert result.json == get_expected_response

# testing multiple challenges
def test_get_total_pythonChallenge(client, jwt_token):
    #get challenge count before test
    responsive = client.get(api_url, headers={'Authorization': f'JWT {jwt_token}'})
    initial_challenge_len = len(responsive.json['challenges'])
    
    #--- start post challenges ---#
    repair_objectiveParamOne = "probando test"
    send_post(client, jwt_token, "valid_code_6.py", "valid_atest_6.py", repair_objectiveParamOne, "1")
    
    repair_objectiveParamTwo = "pruebita test"
    send_post(client, jwt_token, "valid_code_7.py", "valid_atest_7.py", repair_objectiveParamTwo, "2")

    #--- end post challenges ---#
    responsive = client.get(api_url, headers={'Authorization': f'JWT {jwt_token}'})
    data = responsive.json
    
    assert len(data['challenges']) == initial_challenge_len + 2
