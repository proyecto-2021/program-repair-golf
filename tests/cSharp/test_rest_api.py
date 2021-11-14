import os
import pytest
from app import create_app, db
from . import client
from app.cSharp.models import CSharpChallengeModel
import shutil


@pytest.fixture
def create_test_data():
    data = create_challenge('Example1', 'Example1Test', 'Testing', '5', 'BaseExample', 'BaseTest')

    with open('tests/cSharp/test-files/BaseExample.cs') as f:
        content_code = f.read()
    with open('tests/cSharp/test-files/BaseTest.cs') as f:
        content_tests_code = f.read()

    return {'data': data,
            'content_code': content_code,
            'content_tests_code': content_tests_code
            }


def test_post_challenge(client, create_test_data):
    # Arrange
    url = 'cSharp/c-sharp-challenges'

    expected_response = {"challenge":
                         {"code": create_test_data['content_code'],
                          "tests_code": create_test_data['content_tests_code'],
                          "repair_objective": "Testing",
                          "complexity": 5,
                          "best_score": 0
                          }
                         }
    # Act
    response = client.post(url, data=create_test_data['data'])
    response_json = response.json

    # Assert
    assert response.status_code == 200
    del response_json['challenge']['id']
    assert response_json == expected_response

    # Cleanup
    cleanup()


def test_post_with_sintax_error_in_code(client):
    # Arrange
    url = 'cSharp/c-sharp-challenges'
    data = create_challenge('Example1', 'Example1Test', 'Testing', '5', 'ExampleSintaxErrors', 'BaseTest')
    expected_response = {'Challenge': 'Sintax errors'}

    # Act
    response = client.post(url, data=data)

    # Assert
    assert response.status_code == 409
    response_json = response.json
    assert expected_response == response_json

    # Cleanup
    cleanup()


def test_post_challenge_with_incorrect_complexity(client):
    # Arrange
    url = 'cSharp/c-sharp-challenges'
    data = create_challenge('Example1', 'Example1Test', 'Testing', '0', 'BaseExample', 'BaseTest')
    data1 = create_challenge('Example1', 'Example1Test', 'Testing', '6', 'BaseExample', 'BaseTest')
    expected_response = {'Complexity': 'Must be between 1 and 5'}

    # Act
    response = client.post(url, data=data)
    response1 = client.post(url, data=data1)

    # Assert
    assert response.status_code == 409
    assert response1.status_code == 409
    assert expected_response == response.json
    assert expected_response == response1.json

    # Cleanup
    cleanup()


def test_post_challenge_with_sintax_error_in_test(client):
    # Arrange
    url = 'cSharp/c-sharp-challenges'
    data = create_challenge('Example1', 'Example1Test', 'Testing', '3', 'BaseExample', 'TestSintaxErrors')
    expected_response = {'Test': 'Sintax errors'}

    # Act
    response = client.post(url, data=data)

    # Assert
    assert response.status_code == 409
    assert expected_response == response.json

    # Cleanup
    cleanup()


def test_post_challenge_test_no_fails(client):
    # Arrange
    url = 'cSharp/c-sharp-challenges'
    data = create_challenge('Example1', 'Example1Test', 'Testing', '1', 'ExampleNoFails', 'BaseTest')
    expected_response = {'Test': 'At least one has to fail'}

    # Act
    response = client.post(url, data=data)

    # Assert
    assert response.status_code == 409
    assert expected_response == response.json

    # Cleanup
    cleanup()


def test_post_challenge_not_found(client):
    # Arrange
    url = 'cSharp/c-sharp-challenges'
    data = create_challenge('codeDoesNotExist', 'Example1Test', 'Testing', '4', 'BaseTest')
    data1 = create_challenge('Example1', 'TestDoesNotExist', 'Testing', '1', 'BaseExample')
    data2 = create_challenge('codeDoesNotExist', 'TestDoesNotExist', 'Testing', '4')
    data3 = create_challenge('Example1', 'Example1Test', 'Testing', 'BaseExample', 'BaseTest')
    data4 = create_challenge('Example1', 'Example1Test', '2', 'BaseExample', 'BaseTest')
    data5 = create_challenge('Example1', 'Example1Test', 'BaseExample', 'BaseTest')

    expected_response = {"challenge": "Data not found"}
    responses = []

    # Act
    responses.append(client.post(url, data=data))
    responses.append(client.post(url, data=data1))
    responses.append(client.post(url, data=data2))
    responses.append(client.post(url, data=data3))
    responses.append(client.post(url, data=data4))
    responses.append(client.post(url, data=data5))

    # Assert
    for response in responses:
        assert response.status_code == 404
        assert expected_response == response.json

    # Cleanup
    cleanup()


def test_post_repeated_challenge(client):
    # Arrange
    url = 'cSharp/c-sharp-challenges'
    data = create_challenge('Example1', 'Example1Test', 'Testing', '5', 'BaseExample', 'BaseTest')
    data1 = create_challenge('Example1', 'Example1Test', 'Testing', '5', 'BaseExample', 'BaseTest')
    with open('tests/cSharp/test-files/BaseExample.cs') as f:
        content_code = f.read()
    with open('tests/cSharp/test-files/BaseTest.cs') as f:
        content_tests_code = f.read()

    expected_response = {"challenge": {"code": content_code,
                                       "tests_code":  content_tests_code,
                                       "repair_objective": "Testing",
                                       "complexity": 5,
                                       "best_score": 0
                                       }
                         }
    expected_response1 = {'Challenge': 'Already exists'}

    # Act
    response = client.post(url, data=data)
    response1 = client.post(url, data=data1)

    # Assert
    assert response.status_code == 200
    assert response1.status_code == 409
    response_json = response.json
    del response_json['challenge']['id']
    assert expected_response == response_json
    assert expected_response1 == response1.json

    # Cleanup
    cleanup()


def test_get_by_id(client, create_test_data):
    # Arrange
    url = 'cSharp/c-sharp-challenges'
    expected_response = {"Challenge": {"code": create_test_data['content_code'],
                                       "tests_code":  create_test_data['content_tests_code'],
                                       "repair_objective": "Testing",
                                       "complexity": 5,
                                       "best_score": 0
                                       }
                         }
    resp_post = client.post(url, data=create_test_data['data'])
    resp_post_json = resp_post.json
    challenge_id = resp_post_json['challenge']['id']
    url += '/' + str(challenge_id)
    expected_response['Challenge']['id'] = challenge_id

    # Act
    resp_get = client.get(url)
    resp_get_json = resp_get.json

    # Assert
    assert resp_get_json == expected_response
    assert resp_get.status_code == 200

    # Cleanup
    cleanup()


def test_get_non_existent_challenge(client):
    # Arrange
    url = 'cSharp/c-sharp-challenges/1'
    expected_response = {'Challenge': 'Not found'}

    # Act
    resp = client.get(url)
    resp_json = resp.json

    # Assert
    assert resp_json == expected_response
    assert resp.status_code == 404

    # Cleanup
    cleanup()


def test_get_all_challenges_after_post(client, create_test_data):
    # Arrange
    url = 'cSharp/c-sharp-challenges'

    expected_response = {"challenges": [{"code": create_test_data['content_code'],
                                         "tests_code":  create_test_data['content_tests_code'],
                                         "repair_objective": "Testing",
                                         "complexity": 5,
                                         "best_score": 0
                                         }]
                         }
    # Act
    client.post(url, data=create_test_data['data'])
    resp = client.get(url)
    resp_json = resp.json
    print(resp_json)

    # Assert
    assert len(resp_json) == 1
    assert resp.status_code == 200
    del resp_json['challenges'][0]['id']
    assert resp_json == expected_response

    # CleanUp
    cleanup()


def test_get_none_load(client):
    # Arrange
    url = 'cSharp/c-sharp-challenges'
    # Act
    resp = client.get(url)
    # Assert
    assert resp.json == {'challenges': 'None Loaded'}
    assert len(resp.json) == 1
    assert resp.status_code == 200


def test_post_repair(client, create_test_data):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair = {'source_code_file': open('tests/cSharp/test-files/ExampleNoFails.cs', 'rb')}
    
    expected_response = {'Repair': { 'challenge':{
                                                'repair_objective': 'Testing',
                                                'best_score': 2 
                                                },
                                    'score': 2
                                    }
                        }
    
    #Act
    resp_post = client.post(url_post, data=data)
    challenge_id = resp_post.json['challenge']['id'] 

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair = client.post(url_repair, data=data_repair)

    #Assert
    assert resp_repair.status_code == 200
    assert resp_repair.json == expected_response
    #CleanUp
    cleanup()

def test_repair_code_w_sintax_error(client, create_test_data):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair = {'source_code_file': open('tests/cSharp/test-files/ExampleSintaxErrors.cs', 'rb')}
    expected_response = {'Repair candidate': 'Sintax error'}

    #Act
    resp_post = client.post(url_post, data=data)
    challenge_id = resp_post.json['challenge']['id'] 

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair = client.post(url_repair, data=data_repair)

    #Assert
    assert resp_repair.status_code == 409
    assert resp_repair.json == expected_response
    #CleanUp
    cleanup()


def test_repair_challenge_id_not_exist(client, create_test_data):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair = {'source_code_file': open('tests/cSharp/test-files/ExampleNoFails.cs', 'rb')}
    expected_response = {"challenge": "There is no challenge for this id"}
    #Act
    resp_post = client.post(url_post, data=data)
    challenge_id = resp_post.json['challenge']['id'] + 1 

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair = client.post(url_repair, data=data_repair)

    #Assert
    assert resp_repair.status_code == 404
    assert resp_repair.json == expected_response
    #CleanUp
    cleanup()


def test_repair_fails_tests(client, create_test_data):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair = {'source_code_file': open('tests/cSharp/test-files/BaseExample.cs', 'rb')}
    expected_response = {'Repair candidate': 'Tests not passed'}

    #Act
    resp_post = client.post(url_post, data=data)
    challenge_id = resp_post.json['challenge']['id']

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair = client.post(url_repair, data=data_repair)

    #Assert
    assert resp_repair.status_code == 409
    assert resp_repair.json == expected_response

    #CleanUp
    cleanup()


def test_repair_no_file_in_request(client, create_test_data):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair = {}
    expected_response = {'Repair candidate': 'Not found'}

    #Act
    resp_post = client.post(url_post, data=data)
    challenge_id = resp_post.json['challenge']['id']

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair = client.post(url_repair, data=data_repair)

    #Assert
    assert resp_repair.status_code == 404
    assert resp_repair.json == expected_response

    #CleanUp
    cleanup()


def test_post_better_repair(client, create_test_data):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair_1 = {'source_code_file': open('tests/cSharp/test-files/ExampleNoFails.cs', 'rb')}
    data_repair_2 = {'source_code_file': open('tests/cSharp/test-files/ExampleNoFailsLonger.cs', 'rb')}

    #Act
    resp_post = client.post(url_post, data=data)
    challenge_id = resp_post.json['challenge']['id']

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair_1 = client.post(url_repair, data=data_repair_1)
    resp_repair_2 = client.post(url_repair, data=data_repair_2)

    #Assert
    assert resp_repair_1.json['Repair']['challenge']['best_score'] == resp_repair_2.json['Repair']['challenge']['best_score']
    assert resp_repair_1.json['Repair']['score'] < resp_repair_2.json['Repair']['score']

    #CleanUp
    cleanup()


def cleanup():
    db.session.query(CSharpChallengeModel).delete()
    path = "./example-challenges/c-sharp-challenges"
    for dirname in os.listdir(path):
        if os.path.isdir(path + '/' + dirname) and dirname != "Median":
            shutil.rmtree(path + '/' + dirname)


def create_challenge(code_name=None, tests_name=None, repair_objective=None, complexity=None, code=None, tests_code=None):
    challenge = {}
    if code is not None:
        challenge.update({'source_code_file': open(f'tests/cSharp/test-files/{code}.cs', 'rb')})
    if tests_code is not None:
        challenge.update({'test_suite_file': open(f'tests/cSharp/test-files/{tests_code}.cs', 'rb')})

    dict_data = {'source_code_file_name': code_name,
                 'test_suite_file_name': tests_name,
                 'repair_objective': repair_objective,
                 'complexity': complexity}

    challenge.update(challenge_json(dict_data))
    return challenge


def challenge_json(dic_data):
    json_dic = '{ "challenge": { '
    if dic_data[next(iter(dic_data))] is not None:
        first_key = list(dic_data)[0]
    for key in dic_data:
        if dic_data[key] is not None:
            if key == first_key:
                json_dic += f'"{key}" : "{dic_data[key]}"'
            else:
                json_dic += f', "{key}" : "{dic_data[key]}"'

    json_dic += ' } }'
    return {'challenge': json_dic}
