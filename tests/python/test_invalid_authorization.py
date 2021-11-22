from . import client, jwt_token
from .atest_utils import *
import json


# testing of one invalid post challenge
def test_post_pythonChallenge(client, jwt_token):
    repair_objective = "make to pass"
    jwt_token = None
    response = send_post(client, jwt_token, "valid_code_3.py", "valid_atest_3.py", repair_objective, "2", default_code_content=False)
    assert response.status_code == 401

# testing a invalid get single challenge 
def test_get_single_pythonChallenge(client, jwt_token):
    #---- post one challenge to test ---#    
    repair_objectiveParam = "prueba test"
    jwt_token = None
    post_info = send_post(client, jwt_token, "valid_code_5.py", "valid_atest_5.py", repair_objectiveParam, "3")
    if post_info.status_code == 401:
        challenge_id = 10000000
        assert post_info.status_code == 401
    else:
        challenge_id = post_info.json['challenge']['id']
        
    result = client.get(api_url + '/' + str(challenge_id), headers={'Authorization': f'JWT {jwt_token}'})
    #---- end post ---#

    #data to be entered in the post test
    get_expected_response = create_expected_response(0, "valid_code_1.py", "3", 'prueba test', "valid_atest_5.py")

    #data obtained through the get ready for manipulation
    if result.status_code != 401:
        dataChallenge = result.json
        #I get each value within the dictionary
        repair_objective = dataChallenge['challenge']['repair_objective']
        code             = dataChallenge['challenge']['code'] 

    assert result.status_code == 401

# testing a invalid get multiple challenges
def test_get_total_pythonChallenge(client, jwt_token):
    jwt_token = None

    #get challenge count before test
    responsive = client.get(api_url, headers={'Authorization': f'JWT {jwt_token}'})
    if responsive.status_code != 401:
        initial_challenge_len = len(responsive.json['challenges'])
    else:
        assert responsive.status_code == 401

    #--- start post challenges ---#
    repair_objectiveParamOne = "probando test"
    resultOne = send_post(client, jwt_token, "valid_code_6.py", "valid_atest_6.py", repair_objectiveParamOne, "1")

    repair_objectiveParamTwo = "pruebita test"
    resultTwo = send_post(client, jwt_token, "valid_code_7.py", "valid_atest_7.py", repair_objectiveParamTwo, "2")

    #--- end post challenges ---#
    responsive = client.get(api_url, headers={'Authorization': f'JWT {jwt_token}'})
    
    if responsive.status_code != 401:
        data = responsive.json
    
    assert resultOne.status_code == 401
    assert resultTwo.status_code == 401
    assert responsive.status_code == 401

# testing a update python challenge
def test_update_simple_fields(client, jwt_token):
    jwt_token = None

    #make a post and save id
    post_info = send_post(client, jwt_token, "valid_code_8.py", "valid_atest_8.py", "Make all tests pass.", "1")
    if post_info.status_code != 401:
        challenge_id = post_info.json['challenge']['id']
    else:
        challenge_id = 10000000000

    #send an update request
    update_request = request_creator(repair_objective="updated", complexity="3")
    response = client.put(api_url + '/' + str(challenge_id), data=update_request, headers={'Authorization': f'JWT {jwt_token}'})

    update_expected_response = create_expected_response(0, "valid_code_1.py", "3", 'updated', "valid_atest_8.py")

    responseNew = client.get(api_url + '/' + str(challenge_id), headers={'Authorization': f'JWT {jwt_token}'})

    assert response.status_code == 401
    assert responseNew.status_code == 401

def test_update_all(client, jwt_token):
    jwt_token = None

    post_info = send_post(client, jwt_token, "valid_code_13.py", "valid_atest_13.py", "Make all tests pass.", "1")
    if post_info.status_code != 401:
        challenge_id = post_info.json['challenge']['id']
    else:
        challenge_id = 10000000000

    update_request = request_creator(code_path=examples_path + "code_change_my_name_4.py", 
    test_path=examples_path + "atest_change_my_name_4.py", code_name="unique_code_1.py", test_name="unique_atest_1.py")

    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request, headers={'Authorization': f'JWT {jwt_token}'})

    assert update_response.status_code == 401
    assert post_info.status_code == 401
