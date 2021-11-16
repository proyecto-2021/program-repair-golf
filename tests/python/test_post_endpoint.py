from . import client
from .atest_utils import *
import json

# testing of one post challenge
def test_post_pythonChallenge(client):
    repair_objective = "make to pass"
    response = send_post(client, "valid_code_1.py", "valid_atest_1.py", repair_objective, "2")

    assert response.status_code == 200

# testing of post challenge repeated
def test_repeated_post_challenge(client):
    response_one = send_post(client, "valid_code_1.py", "valid_atest_1.py", "make to pass", "2")
    response_two = send_post(client, "valid_code_1.py", "valid_atest_3.py", "make to pass", "2")

    assert response_two == 409
    assert response_two.json['Error'] == "Another code with that name already exists"

def test_post_challenge_invalid_code(client):
    response = send_post(client, "code_not_compile.py", "valid_atest_1.py", "Make all tests pass.", "2")

    assert response.status_code == 409
    #get json with the error
    json_response = response.json
    assert json_response['Error'] == 'Syntax error at ' + 'code_not_compile.py'

def test_post_challenge_invalid_test(client):
    response = send_post(client, "valid_code_1.py", "atest_not_compile.py", "Make all tests pass.", "2")

    assert response.status_code == 409
    #get json with the error
    json_response = response.json
    assert json_response['Error'] == 'Syntax error at ' + 'atest_not_compile.py'

def test_post_challenge_binarycode_empty(client):
    response = send_post(client, "", "valid_atest_1.py", "Make all tests pass.", "2")
    assert response == 400

def test_post_challenge_binarycodetest_empty(client):
    response = send_post(client, "valid_code_1.py", " ", "Make all tests pass.", "2")
    assert response == 400

#post challenge with no errors in tests (so its repaired)
def test_post_invalid_repaired_challenge(client):
    response = send_post(client, "code_repair_2.py", "valid_atest_2.py", "Make all tests pass.", "2")

    assert response.status_code == 409
    #get json with the error
    json_response = response.json
    assert json_response['Error'] == 'At least one test must fail'