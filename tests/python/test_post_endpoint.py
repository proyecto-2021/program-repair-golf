from . import client, jwt_token
from .atest_utils import *
import json

# testing of one post challenge
def test_post_pythonChallenge(client, jwt_token):
    repair_objective = "make to pass"
    response = send_post(client, jwt_token, "valid_code_3.py", "valid_atest_3.py", repair_objective, "2", default_code_content=False)

    assert response.status_code == 200

# testing of post challenge repeated
def test_repeated_post_challenge(client, jwt_token):
    response_one = send_post(client, jwt_token, "valid_code_1.py", "valid_atest_1.py", "make to pass", "2")
    response_two = send_post(client, jwt_token, "valid_code_1.py", "valid_atest_3.py", "make to pass", "2")

    assert response_two.status_code == 409
    assert response_two.json['Error'] == "Another code with that name already exists"

def test_post_challenge_invalid_code(client, jwt_token):
    response = send_post(client, jwt_token, "code_not_compile.py", "valid_atest_4.py", "Make all tests pass.", "2", default_code_content=False)

    assert response.status_code == 409
    #get json with the error
    json_response = response.json
    assert json_response['Error'] == 'Syntax error at ' + 'code_not_compile.py'

def test_post_challenge_invalid_test(client, jwt_token):
    response = send_post(client, jwt_token, "valid_code_4.py", "atest_not_compile.py", "Make all tests pass.", "2")

    assert response.status_code == 409
    #get json with the error
    json_response = response.json
    assert json_response['Error'] == 'Syntax error at ' + 'atest_not_compile.py'

def test_post_challenge_binarycode_empty(client, jwt_token):
    dataChallengePost = request_creator(code_name="valid_code_1.py", test_name="valid_atest_1.py", 
    test_path=examples_path + "valid_atest_1.py", repair_objective="Make all tests pass.", complexity="2")
    
    response = client.post(api_url, data=dataChallengePost, headers={'Authorization': f'JWT {jwt_token}'})
    
    assert response.status_code == 409
    assert response.json['Error'] == 'Source code, test code or general data were not provided'
    
def test_post_challenge_binarycodetest_empty(client, jwt_token):
    dataChallengePost = request_creator(code_name="valid_code_1.py", test_name="valid_atest_1.py", 
    code_path=examples_path + "valid_code_1.py", repair_objective="Make all tests pass.", complexity="2")
    
    response = client.post(api_url, data=dataChallengePost, headers={'Authorization': f'JWT {jwt_token}'})
    
    assert response.status_code == 409
    assert response.json['Error'] == 'Source code, test code or general data were not provided'
    
#post challenge with no errors in tests (so its repaired)
def test_post_invalid_repaired_challenge(client, jwt_token):
    response = send_post(client, jwt_token, "code_repair_2.py", "valid_atest_2.py", "Make all tests pass.", "2", default_code_content=False)

    assert response.status_code == 409
    #get json with the error
    json_response = response.json
    assert json_response['Error'] == 'At least one test must fail'