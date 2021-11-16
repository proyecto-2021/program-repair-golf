from app.python.models import *
from . import client
from .atest_utils import *
import json



def test_get_challenge_not_found(client):
    
    invalid_id = 1000000000000000
    result = client.get(api_url + '/' + str(invalid_id))

    assert result.status_code == 409
    assert result.json['Error'] == "Challenge not found"

# testing a single challenge 
def test_get_single_pythonChallenge(client):
    #---- post one challenge to test ---#    
    repair_objectiveParam = "prueba test"
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", repair_objectiveParam, "3")
    
    challenge_id = post_info.json['challenge']['id']
    result = client.get(api_url + '/' + str(challenge_id))
    #---- end post ---#

    #data to be entered in the post test
    post_expected_response = create_expected_response(0, "valid_code_1.py", "3", 'prueba test', "valid_atest_1.py")

    #data obtained through the get ready for manipulation
    dataChallenge = result.json

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
    initial_challenge_len = len(responsive.json['challenges'])
    
    #--- start post challenges ---#
    repair_objectiveParamOne = "probando test"
    send_post(client, "valid_code_1.py", "valid_atest_1.py", repair_objectiveParamOne, "1")
    
    repair_objectiveParamTwo = "pruebita test"
    send_post(client, "valid_code_1.py", "valid_atest_1.py", repair_objectiveParamTwo, "2")

    #--- end post challenges ---#
    responsive = client.get(api_url)
    data = responsive.json
    
    assert len(data['challenges']) == initial_challenge_len + 2

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

def test_update_simple_fields(client):
    #make a post and save id
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", "Make all tests pass.", "1")
    challenge_id = post_info.json['challenge']['id']
    #send an update request
    update_request = request_creator(repair_objective="updated", complexity="3")
    response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    update_expected_response = create_expected_response(0, "valid_code_1.py", "3", 'updated', "valid_atest_1.py")

    assert response.status_code == 200
    assert response.json == update_expected_response
    #check te same with get
    response = client.get(api_url + '/' + str(challenge_id))
    assert response.json == update_expected_response

def test_update_valid_code(client):
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", "Make all tests pass.", "1")

    challenge_id = post_info.json['challenge']['id']
    #send an update request
    update_request = request_creator(code_path=examples_path + "valid_code_3.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 200
    #the file has been saved correctly
    assert update_response.json['challenge']['code'] == read_file(examples_path + 'valid_code_3.py', 'r')

def test_update_not_compiling_code(client):
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", "Make all tests pass.", "1")

    challenge_id = post_info.json['challenge']['id']
    #send an update request
    update_request = request_creator(code_path=examples_path + "code_not_compile.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409
    #the filename hasn't changed, its the same we used for post
    assert update_response.json['Error'] == 'Syntax error at ' + 'valid_code_1.py'

    
def test_update_repaired_code(client):
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", "Make all tests pass.", "1")

    challenge_id = post_info.json['challenge']['id']
    #send an update request with repaired code
    update_request = request_creator(code_path=examples_path + "code_repair_2.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409
    #the filename hasn't changed, its the same we used for post
    assert update_response.json['Error'] == 'At least one test must fail'

def test_update_test_invalid_import(client):
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", "Make all tests pass.", "1")
    challenge_id = post_info.json['challenge']['id']

    update_request = request_creator(test_path=examples_path + "import_error_atest.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409
    
    assert update_response.json['Error'] == "Import error, tests can't run"

def test_update_code_name_fails(client):
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", "Make all tests pass.", "1")
    challenge_id = post_info.json['challenge']['id']
    
    #updating to a name that already exists
    update_request = request_creator(code_name="valid_code_3.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409   #should get error for name conflict
    assert update_response.json['Error'] == "Another challenge with that name already exists"

    #updating to a name that doesn't exists
    update_request = request_creator(code_name="another_unique_name.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409   #test will not find that file to import
    assert update_response.json['Error'] == "Import error, tests can't run"

def test_update_code_name_fails(client):
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", "Make all tests pass.", "1")
    challenge_id = post_info.json['challenge']['id']
    
    #updating to a name that already exists
    update_request = request_creator(code_name="valid_code_3.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409   #should get error for name conflict
    assert update_response.json['Error'] == "Another challenge with that name already exists"

    #updating to a name that doesn't exists
    update_request = request_creator(code_name="another_unique_name.py")
    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409   #test will not find that file to import
    assert update_response.json['Error'] == "Import error, tests can't run"

def test_update_all(client):
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", "Make all tests pass.", "1")
    challenge_id = post_info.json['challenge']['id']

    update_request = request_creator(code_path=examples_path + "code_change_my_name_4.py", 
    test_path=examples_path + "atest_change_my_name_4.py", code_name="unique_code_1.py", test_name="unique_atest_1.py")

    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 200

    assert read_file("public/challenges/unique_code_1.py", "r") == update_response.json['challenge']['code']
    assert read_file("public/challenges/unique_atest_1.py", "r") == update_response.json['challenge']['tests_code']

def test_update_all_code_name_conflict(client):
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", "Make all tests pass.", "1")
    challenge_id = post_info.json['challenge']['id']
    #code name is not the same as the new test is importing
    update_request = request_creator(code_path=examples_path + "code_change_my_name_4.py", 
    test_path=examples_path + "atest_change_my_name_4.py", code_name="test_will_not_find_me.py", test_name="unique_atest_1.py")

    update_response = client.put(api_url + '/' + str(challenge_id), data=update_request)

    assert update_response.status_code == 409
    assert  update_response.json['Error'] == "Import error, tests can't run"

def test_post_repair_challenge(client):

    repair_objectiveParam = "Test repair"
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", repair_objectiveParam, '3')

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
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", repair_objectiveParam, '3')
    challenge_id = post_info.json['challenge']['id']
    
    response = client.post(api_url + '/' + str(challenge_id) + '/repair')

    assert response.status_code == 409
    assert response.json['Error'] == "No repair provided"

def test_post_repair_update_best_score(client):

    repair_objectiveParam = "Test repair"
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", repair_objectiveParam, '3')

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
    post_info = send_post(client, "valid_code_1.py", "valid_atest_1.py", repair_objectiveParam, '3')

    challenge_id = post_info.json['challenge']['id']

    repair_request = request_creator(code_path = examples_path + "code_repair_atest_fail.py")

    response = client.post(api_url + '/' + str(challenge_id) + '/repair', data = repair_request)

    assert response.status_code == 409
    assert response.json['Error'] == "Some test failed"

