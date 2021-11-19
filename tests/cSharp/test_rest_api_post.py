import os
import pytest
from app import create_app, db
from . import *
import shutil

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
    data0 = {}
    data = create_challenge(tests_name='Example1Test',
                            repair_objective='Testing',
                            complexity='4', tests_code='BaseTest')
    data1 = create_challenge(code_name='Example1', repair_objective='Testing',
                             complexity='1', code='BaseExample')
    data2 = create_challenge(repair_objective='Testing', complexity='4')
    data3 = create_challenge(code_name='Example1', tests_name='Example1Test',
                             repair_objective='Testing', code='BaseExample',
                             tests_code='BaseTest')
    data4 = create_challenge(code_name='Example1', tests_name='Example1Test',
                             complexity='2', code='BaseExample',
                             tests_code='BaseTest')
    data5 = create_challenge(code_name='Example1', tests_name='Example1Test',
                             code='BaseExample', tests_code='BaseTest')

    expected_response = {"challenge": "Data not found"}
    responses = []

    # Act
    responses.append(client.post(url, data=data0))
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