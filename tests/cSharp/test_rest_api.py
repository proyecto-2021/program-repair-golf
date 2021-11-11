import os
import pytest
from app import create_app, db
from . import client
from app.cSharp.models import CSharpChallengeModel
import shutil


def test_post_challenge(client):
    #Arrange
    url = 'cSharp/c-sharp-challenges'
    data = create_challenge('Example1', 'Example1Test', 'Testing', '5', 'Example1', 'Example1Test')

    with open('tests/cSharp/test-files/Example1.cs') as f:
        content_code = f.read()
    with open('tests/cSharp/test-files/Example1Test.cs') as f:
        content_tests_code = f.read()
    expected_response = {"challenge": { "code": content_code,
                                        "tests_code":  content_tests_code,
                                        "repair_objective": "Testing",
                                        "complexity": 5,
                                        "best_score": 0
                                       }
                        }
    #Act
    response = client.post(url, data=data)
    response_json = response.json

    #Assert
    assert response.status_code == 200
    del response_json['challenge']['id']
    assert response_json == expected_response

    #Cleanup
    cleanup()

def test_post_with_sintax_error_in_code(client):
    #Arrange
    url = 'cSharp/c-sharp-challenges'
    data = create_challenge('Example2', 'Example2Test', 'Testing', '3', 'Example2', 'Example2Test')
    expected_response = {'Challenge': 'Sintax errors'}
    
    #Act
    response = client.post(url, data=data)

    #Aassert
    assert response.status_code == 409
    response_json = response.json
    assert  expected_response == response_json
    
    #Cleanup
    cleanup()

def test_post_challenge_with_incorrect_complexity(client):
    #Arrange
    url = 'cSharp/c-sharp-challenges'
    data = create_challenge('Example1', 'Example1Test', 'Testing', '0', 'Example1', 'Example1Test')
    data1 =create_challenge('Example01', 'Example01Test', 'Testing', '6', 'Example01', 'Example01Test')
    expected_response = {'Complexity': 'Must be between 1 and 5'}
    
    #Act
    response = client.post(url, data=data)
    response1 = client.post(url, data=data1)

    #Assert
    assert response.status_code == 409
    assert response1.status_code == 409
    response_json = response.json
    response1_json = response1.json
    assert  expected_response == response_json
    assert  expected_response == response1_json

    #Cleanup
    cleanup()

def test_post_challenge_with_sintax_error_in_test(client):
    #Arrange
    url = 'cSharp/c-sharp-challenges'
    data = create_challenge('Example3', 'Example3Test', 'Testing', '3', 'Example3', 'Example3Test')
    expected_response = {'Test': 'Sintax errors'}
    
    #Act
    response = client.post(url, data=data)

    #Aassert
    assert response.status_code == 409
    response_json = response.json
    assert  expected_response == response_json

    #Cleanup
    cleanup()

def test_post_challenge_test_no_fails(client):
    #Arrange
    url = 'cSharp/c-sharp-challenges'
    data = create_challenge('Example4', 'Example4Test', 'Testing', '1', 'Example4', 'Example4Test')
    expected_response = {'Test': 'At least one has to fail'}
    
    #Act
    response = client.post(url, data=data)

    #Aassert
    assert response.status_code == 409
    response_json = response.json
    assert  expected_response == response_json

    #Cleanup
    cleanup()
    



def cleanup():
    db.session.query(CSharpChallengeModel).delete()
    path = "./example-challenges/c-sharp-challenges"
    for dirname in os.listdir(path):
        if dirname != "Median":
            shutil.rmtree(path + '/' + dirname)


def create_challenge(code_name=None, tests_name=None, repair_objective=None, complexity=None, code=None, tests_code=None):
    challenge = {}
    if code is not None:
        challenge.update({'source_code_file': open(f'tests/cSharp/test-files/{code}.cs', 'rb')})
    if tests_code is not None:
        challenge.update({'test_suite_file': open(f'tests/cSharp/test-files/{tests_code}.cs', 'rb')})

    dict_data = { 'source_code_file_name': code_name, 'test_suite_file_name': tests_name, 'repair_objective': repair_objective, 'complexity': complexity }
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






