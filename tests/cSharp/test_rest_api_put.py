import os
import pytest
from app import create_app, db
from . import *
from app.cSharp.models import CSharpChallengeModel
import shutil

def test_update_incorrect_complexity(client, create_test_data, auth):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']

    data_put = create_challenge(complexity=8)
    #Act
    resp_post = client.post(url_post, data=data, headers={'Authorization': f'JWT {auth}'})
    challenge_id = resp_post.json['challenge']['id']
    
    url_put = 'cSharp/c-sharp-challenges/' + str(challenge_id) 
    resp_put = client.put(url_put, data=data_put, headers={'Authorization': f'JWT {auth}'})

    #Assert
    assert resp_put.status_code == 409
    assert resp_put.json == {'Complexity': 'Must be between 1 and 5'}
    cleanup()

def test_update_code_w_sintax_error(client,create_test_data, auth):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_put = {'source_code_file': open('tests/cSharp/test-files/ExampleSintaxErrors.cs', 'rb')}
    
    #Act
    resp_post = client.post(url_post, data=data, headers={'Authorization': f'JWT {auth}'})
    challenge_id = resp_post.json['challenge']['id'] 

    url_put = 'cSharp/c-sharp-challenges/' + str(challenge_id) 
    resp_put = client.put(url_put, data=data_put, headers={'Authorization': f'JWT {auth}'})
    
    #Assert
    assert resp_put.status_code == 409
    assert resp_put.json == {'Source code': 'Sintax errors'}
    cleanup()

def test_update_complexity_and_repair_objective(client, create_test_data, auth):
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_put = create_challenge(repair_objective='Test this method', complexity='4')
    expected_response = {"challenge": { "code": create_test_data['content_code'],
                                        "tests_code":  create_test_data['content_tests_code'],
                                        "repair_objective": "Test this method",
                                        "complexity": 4,
                                        "best_score": 0
                                       }
                        }

    resp_post = client.post(url_post, data=data, headers={'Authorization': f'JWT {auth}'})
    challenge_id = resp_post.json['challenge']['id']
     
    url_put = 'cSharp/c-sharp-challenges/' + str(challenge_id) 
    resp_put = client.put(url_put, data=data_put, headers={'Authorization': f'JWT {auth}'})
    resp_put_json = resp_put.json
    del resp_put_json['challenge']['id']
    print(resp_put.json)
    
    #Assert
    assert resp_put.status_code == 200
    assert resp_put_json == expected_response
    cleanup()

def test_update_code_passes_all_tests(client, create_test_data, auth):
    # Arrange
    url = 'cSharp/c-sharp-challenges'

    data_put = create_challenge(code_name='Example1', code='ExampleNoFails')
    expected_response = {'Challenge': 'Must fail at least one test'}

    # Act
    resp_post = client.post(url, data=create_test_data['data'], headers={'Authorization': f'JWT {auth}'})
    ch_id = resp_post.json['challenge']['id']
    url += '/' + str(ch_id)

    resp_put = client.put(url, data=data_put, headers={'Authorization': f'JWT {auth}'})
    resp_json = resp_put.json
    resp_code = resp_put.status_code

    # Assert
    assert resp_code == 409
    assert resp_json == expected_response

    # Cleanup
    cleanup()


def test_put_non_existent_challenge(client, auth):
    # Arrange
    url = 'cSharp/c-sharp-challenges/1'
    expected_response = {"challenge": "There is no challenge for this id"}
    data_put={}

    # Act
    resp = client.put(url, data=data_put, headers={'Authorization': f'JWT {auth}'})
    resp_json = resp.json

    # Assert
    assert resp_json == expected_response
    assert resp.status_code == 404

    # Cleanup
    cleanup()

def test_put_with_code_and_test_and_without_challenge(client, create_test_data, auth):
    # Arrange
    url = 'cSharp/c-sharp-challenges'
    data_post = create_test_data['data']
    data_put = create_challenge(code="BaseExample3", tests_code="BaseTest3")
    with open('tests/cSharp/test-files/BaseExample3.cs') as f:
        new_content_code = f.read()
    with open('tests/cSharp/test-files/BaseTest3.cs') as f:
        new_content_tests_code = f.read()

    # Act
    resp_post = client.post(url, data=data_post, headers={'Authorization': f'JWT {auth}'})
    challenge_id = resp_post.json["challenge"]["id"]
    url_put = 'cSharp/c-sharp-challenges/' + str(challenge_id)
    resp_put = client.put(url_put, data=data_put, headers={'Authorization': f'JWT {auth}'})

    # Assert
    resp_put_json = resp_put.json
    del resp_put_json ['challenge']['id']
    
    assert resp_put.status_code == 200
    assert resp_put_json == {"challenge": { "best_score": 0,
                                            "code": new_content_code,
                                            "complexity": 5,
                                            "repair_objective": "Testing",
                                            "tests_code":new_content_tests_code                                                  
                                          }
                            }
    
    # Cleanup
    cleanup()

def test_put_with_only_test(client, create_test_data, auth):
    # Arrange
    url = 'cSharp/c-sharp-challenges'

    data_post = create_test_data['data']
    data_put = create_challenge(tests_name='Example1Test', tests_code="BaseTest")
    with open('tests/cSharp/test-files/BaseTest.cs') as f:
        new_content_tests_code = f.read()
    expected_response = {"challenge": { "best_score": 0,
                                        "code":create_test_data['content_code'],
                                        "complexity": 5,
                                        "repair_objective": "Testing",
                                        "tests_code":new_content_tests_code                                                  
                                       }
                        }
    # Act
    resp_post = client.post(url, data=data_post, headers={'Authorization': f'JWT {auth}'})
    challenge_id = resp_post.json["challenge"]["id"]
    url_put = 'cSharp/c-sharp-challenges/' + str(challenge_id)
    resp_put = client.put(url_put, data=data_put, headers={'Authorization': f'JWT {auth}'})
    # Assert
    resp_put_json = resp_put.json
    del resp_put_json ['challenge']['id']
    
    assert resp_put.status_code == 200
    assert resp_put_json == expected_response
    
    # Cleanup
    cleanup()

def test_update_test_with_sintax_error(client, create_test_data, auth):
    # Arrange
    url = 'cSharp/c-sharp-challenges'

    data_put = create_challenge(tests_name='Example1Test', tests_code='TestSintaxErrors')
    expected_response = {'Test': 'Sintax errors'}

    # Act
    resp_post = client.post(url, data=create_test_data['data'], headers={'Authorization': f'JWT {auth}'})
    ch_id = resp_post.json['challenge']['id']
    url += '/' + str(ch_id)

    resp_put = client.put(url, data=data_put, headers={'Authorization': f'JWT {auth}'})
    resp_json = resp_put.json
    resp_code = resp_put.status_code

    # Assert
    assert resp_code == 409
    assert resp_json == expected_response

    # Cleanup
    cleanup()


def test_update_code_and_test_not_valid(client, create_test_data, auth):
    # Arrange
    url = 'cSharp/c-sharp-challenges'
    data_put_1 = create_challenge(code="ExampleSintaxErrors", tests_code="BaseTest")
    data_put_2 = create_challenge(code="ExampleNoFails", tests_code="BaseTest")
    data_put_3 = create_challenge(code="BaseExample", tests_code="TestSintaxErrors")

    expected_response_1 = {'Source code': 'Sintax errors'}
    expected_response_2 = {'Challenge': 'Must fail at least one test'}
    expected_response_3 = {'Test': 'Sintax errors'}

    resp_post = client.post(url, data=create_test_data['data'], headers={'Authorization': f'JWT {auth}'})
    ch_id = resp_post.json['challenge']['id']
    url += '/' + str(ch_id)

    # Act
    resp_put_1 = client.put(url, data=data_put_1, headers={'Authorization': f'JWT {auth}'})
    resp_put_2 = client.put(url, data=data_put_2, headers={'Authorization': f'JWT {auth}'})
    resp_put_3 = client.put(url, data=data_put_3, headers={'Authorization': f'JWT {auth}'})

    resp_json_1 = resp_put_1.json
    resp_json_2 = resp_put_2.json
    resp_json_3 = resp_put_3.json

    response_codes = (resp_put_1.status_code,
                      resp_put_2.status_code,
                      resp_put_3.status_code)

    # Assert
    assert all(response == 409 for response in response_codes)
    assert resp_json_1 == expected_response_1
    assert resp_json_2 == expected_response_2
    assert resp_json_3 == expected_response_3

    # Cleanup
    cleanup()


def test_update_invalid_code(client, create_test_data, auth):
     # Arrange
    url = 'cSharp/c-sharp-challenges'

    data_put_1 = create_challenge(code='ExampleSintaxErrors')
    data_put_2 = create_challenge(code='ExampleNoFails')
    data_put_3 = create_challenge(code='BaseExample3')

    expected_response_1 = {'Source code': 'Sintax errors'}
    expected_response_2 = {'Challenge': 'Must fail at least one test'}
    expected_response_3 = {'Test': 'Sintax errors'}

    # Act
    resp_post = client.post(url, data=create_test_data['data'], headers={'Authorization': f'JWT {auth}'})
    ch_id = resp_post.json['challenge']['id']
    url += '/' + str(ch_id)

    # Act
    resp_put_1 = client.put(url, data=data_put_1, headers={'Authorization': f'JWT {auth}'})
    resp_put_2 = client.put(url, data=data_put_2, headers={'Authorization': f'JWT {auth}'})
    resp_put_3 = client.put(url, data=data_put_3, headers={'Authorization': f'JWT {auth}'})

    resp_json_1 = resp_put_1.json
    resp_json_2 = resp_put_2.json
    resp_json_3 = resp_put_3.json

    response_codes = (resp_put_1.status_code,
                      resp_put_2.status_code,
                      resp_put_3.status_code)

    # Assert
    assert all(response == 409 for response in response_codes)
    assert resp_json_1 == expected_response_1
    assert resp_json_2 == expected_response_2
    assert resp_json_3 == expected_response_3

    # Cleanup
    cleanup()
