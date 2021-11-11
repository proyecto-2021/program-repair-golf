import os
import pytest
from app import create_app, db
from . import client
from app.cSharp.models import CSharpChallengeModel
import shutil


def test_post_challenge(client):
    #arrange
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
    #act
    response = client.post(url, data=data)
    response_json = response.json
    assert response.status_code == 200
    del response_json['challenge']['id']
    assert response_json == expected_response
    cleanup()


def test_get_all_challenges_after_post(client):
    #Arrange
    url = 'cSharp/c-sharp-challenges'
    data = create_challenge('Example5', 'Example5Test', 'Testing', '5', 'Example5', 'Example5Test')

    with open('tests/cSharp/test-files/Example5.cs') as f:
        content_code = f.read()
    with open('tests/cSharp/test-files/Example5Test.cs') as f:
        content_tests_code = f.read()

    expected_response = {'challenges': [{"code": content_code,
                                        "tests_code": content_tests_code,
                                        "repair_objective": "Testing",
                                        "complexity": 5,
                                        "best_score": 0
                                    }]
                        }
    #Act
    client.post(url, data=data)
    resp = client.get(url)
    resp_json = resp.json

    #Assert
    assert len(resp_json) == 1
    assert resp.status_code == 200
    del resp_json['challenges'][0]['id']
    assert resp_json == expected_response

    #CleanUp
    db.session.query(CSharpChallengeModel).delete()


def test_get_none_load(client):
    #Arrange
    url = 'cSharp/c-sharp-challenges'
    #Act
    resp = client.get(url)
    #Assert
    assert resp.json == {'challenges': 'None Loaded'}
    assert len(resp.json) == 1 
    assert resp.status_code == 200


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
