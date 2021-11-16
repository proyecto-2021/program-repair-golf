from . import client
from .atest_utils import *
import json


def test_update_simple_fields(client):
    #make a post and save id
    post_info = send_post(client, "valid_code_8.py", "valid_atest_8.py", "Make all tests pass.", "1")
    challenge_id = post_info.json['challenge']['id']
    #send an update request
    update_request = request_creator(repair_objective="updated", complexity="3")
    response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    update_expected_response = create_expected_response(0, "valid_code_1.py", "3", 'updated', "valid_atest_8.py")

    assert response.status_code == 200
    assert response.json == update_expected_response
    #check te same with get
    response = client.get(api_url + '/' + str(challenge_id))
    assert response.json == update_expected_response

def test_update_valid_code(client):
    post_info = send_post(client, "valid_code_9.py", "valid_atest_9.py", "Make all tests pass.", "1")

    challenge_id = post_info.json['challenge']['id']
    #send an update request
    update_request = request_creator(code_path=examples_path + "valid_code_4.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 200
    #the file has been saved correctly
    assert update_response.json['challenge']['code'] == read_file(examples_path + 'valid_code_4.py', 'r')

def test_update_not_compiling_code(client):
    post_info = send_post(client, "valid_code_10.py", "valid_atest_10.py", "Make all tests pass.", "1")

    challenge_id = post_info.json['challenge']['id']
    #send an update request
    update_request = request_creator(code_path=examples_path + "code_not_compile.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409
    #the filename hasn't changed, its the same we used for post
    assert update_response.json['Error'] == 'Syntax error at ' + 'valid_code_10.py'

    
def test_update_repaired_code(client):
    post_info = send_post(client, "valid_code_11.py", "valid_atest_11.py", "Make all tests pass.", "1")

    challenge_id = post_info.json['challenge']['id']
    #send an update request with repaired code
    update_request = request_creator(code_path=examples_path + "code_repair_2.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409
    #the filename hasn't changed, its the same we used for post
    assert update_response.json['Error'] == 'At least one test must fail'

def test_update_test_invalid_import(client):
    post_info = send_post(client, "valid_code_12.py", "valid_atest_12.py", "Make all tests pass.", "1")
    challenge_id = post_info.json['challenge']['id']

    update_request = request_creator(test_path=examples_path + "import_error_atest.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409
    
    assert update_response.json['Error'] == "Import error, tests can't run"

def test_update_code_name_fails(client):
    post_info = send_post(client, "valid_code_19.py", "valid_atest_19.py", "Make all tests pass.", "1")
    challenge_id = post_info.json['challenge']['id']
    post_info = send_post(client, "valid_code_20.py", "valid_atest_20.py", "Make all tests pass.", "1")
    
    #updating to a name that already exists
    update_request = request_creator(code_name="valid_code_20.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409   #should get error for name conflict
    assert update_response.json['Error'] == "Another code with that name already exists"

    #updating to a name that doesn't exists
    update_request = request_creator(code_name="another_unique_name.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409   #test will not find that file to import
    assert update_response.json['Error'] == "Import error, tests can't run"

def test_update_all(client):
    post_info = send_post(client, "valid_code_13.py", "valid_atest_13.py", "Make all tests pass.", "1")
    challenge_id = post_info.json['challenge']['id']

    update_request = request_creator(code_path=examples_path + "code_change_my_name_4.py", 
    test_path=examples_path + "atest_change_my_name_4.py", code_name="unique_code_1.py", test_name="unique_atest_1.py")

    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 200

    assert read_file("public/challenges/unique_code_1.py", "r") == update_response.json['challenge']['code']
    assert read_file("public/challenges/unique_atest_1.py", "r") == update_response.json['challenge']['tests_code']

def test_update_all_code_name_conflict(client):
    post_info = send_post(client, "valid_code_14.py", "valid_atest_14.py", "Make all tests pass.", "1")
    challenge_id = post_info.json['challenge']['id']
    #code name is not the same as the new test is importing
    update_request = request_creator(code_path=examples_path + "code_change_my_name_4.py", 
    test_path=examples_path + "atest_change_my_name_4.py", code_name="test_will_not_find_me.py", test_name="unique_atest_2.py")

    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409
    assert  update_response.json['Error'] == "Import error, tests can't run"
