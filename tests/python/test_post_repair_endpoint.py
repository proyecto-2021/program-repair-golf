from . import client
from .atest_utils import *
import json

def test_post_repair_challenge(client):

    repair_objectiveParam = "Test repair"
    post_info = send_post(client, "valid_code_15.py", "valid_atest_15.py", repair_objectiveParam, '3')

    challenge_id = post_info.json['challenge']['id']

    repair_request = request_creator(code_path = examples_path + "code_repair_2.py")

    response = client.post(api_url + '/' + str(challenge_id) + '/repair', data = repair_request)

    assert response.status_code == 200
    json_response = response.json
    assert json_response['repair']['score'] == 2

def test_post_repair_challenge_invalid(client):
    
    repair_request = request_creator(code_path = examples_path + "code_repair_2.py")
    
    invalid_id = 1000000000000000

    response = client.post(api_url + '/' + str(invalid_id) + '/repair', data = repair_request)
    
    assert response.status_code == 409
    assert response.json['Error'] == "Challenge not found"

def test_post_repair_code_not_provided(client):
    
    repair_objectiveParam = "Test repair"
    post_info = send_post(client, "valid_code_16.py", "valid_atest_16.py", repair_objectiveParam, '3')
    challenge_id = post_info.json['challenge']['id']
    
    response = client.post(api_url + '/' + str(challenge_id) + '/repair')

    assert response.status_code == 409
    assert response.json['Error'] == "No repair provided"

def test_post_repair_update_best_score(client):

    repair_objectiveParam = "Test repair"
    post_info = send_post(client, "valid_code_17.py", "valid_atest_17.py", repair_objectiveParam, '3')

    challenge_id = post_info.json['challenge']['id']

    repair_request = request_creator(code_path = examples_path + "code_repair_2.py")
    repair_request_2 = request_creator(code_path = examples_path + "code_repair_2.py")

    response = client.post(api_url + '/' + str(challenge_id) + '/repair', data = repair_request)

    old_best_score = response.json['repair']['challenge']['best_score']

    response = client.post(api_url + '/' + str(challenge_id) + '/repair', data = repair_request_2)

    assert response.status_code == 200
    assert response.json['repair']['challenge']['best_score'] >= old_best_score

def test_post_repair_not_past_tests(client):
    
    repair_objectiveParam = "Test repair"
    post_info = send_post(client, "valid_code_18.py", "valid_atest_18.py", repair_objectiveParam, '3')

    challenge_id = post_info.json['challenge']['id']

    repair_request = request_creator(code_path = examples_path + "code_repair_atest_fail.py")

    response = client.post(api_url + '/' + str(challenge_id) + '/repair', data = repair_request)

    assert response.status_code == 409
    assert response.json['Error'] == "Some test failed"

