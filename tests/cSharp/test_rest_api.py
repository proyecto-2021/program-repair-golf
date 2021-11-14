import os
import pytest
from app import create_app, db
from . import client
from app.cSharp.models import CSharpChallengeModel
import shutil

@pytest.fixture
def create_test_data():
    data = create_challenge('Example1', 'Example1Test', 'Testing', '5', 'Example1', 'Example1Test')

    with open('tests/cSharp/test-files/Example1.cs') as f:
        content_code = f.read()
    with open('tests/cSharp/test-files/Example1Test.cs') as f:
        content_tests_code = f.read()
    
    return {'data':data, 
            'content_code':content_code,
            'content_tests_code':content_tests_code
            }

def test_post_challenge(client, create_test_data):
    #arrange
    url = 'cSharp/c-sharp-challenges'
    
    expected_response = {"challenge": { "code": create_test_data['content_code'],
                                        "tests_code":  create_test_data['content_tests_code'],
                                        "repair_objective": "Testing",
                                        "complexity": 5,
                                        "best_score": 0
                                       }
                        }
    #act
    response = client.post(url, data=create_test_data['data'])
    response_json = response.json

    assert response.status_code == 200
    del response_json['challenge']['id']
    assert response_json == expected_response
    cleanup()


def test_get_all_challenges_after_post(client, create_test_data):
    #Arrange
    url = 'cSharp/c-sharp-challenges'

    expected_response = {"challenges": [{ "code": create_test_data['content_code'],
                                        "tests_code":  create_test_data['content_tests_code'],
                                        "repair_objective": "Testing",
                                        "complexity": 5,
                                        "best_score": 0
                                       }]
                        }
    #Act
    client.post(url, data=create_test_data['data'])
    resp = client.get(url)
    resp_json = resp.json
    print(resp_json)

    #Assert
    assert len(resp_json) == 1
    assert resp.status_code == 200
    del resp_json['challenges'][0]['id']
    assert resp_json == expected_response

    #CleanUp
    cleanup()


def test_get_none_load(client):
    #Arrange
    url = 'cSharp/c-sharp-challenges'
    #Act
    resp = client.get(url)
    #Assert
    assert resp.json == {'challenges': 'None Loaded'}
    assert len(resp.json) == 1 
    assert resp.status_code == 200


def test_post_repair(client, create_test_data):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair = {'source_code_file': open('tests/cSharp/test-files/Example1Repair.cs', 'rb')}
    
    expected_response = {'repair': { 'challenge':{
                                                'repair_objective': 'Testing',
                                                'best_score': 3 
                                                },
                                    'score': 3
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
    data_repair = {'source_code_file': open('tests/cSharp/test-files/Example2.cs', 'rb')}
    expected_response = {'repair candidate:': 'Sintax error'}

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
    data_repair = {'source_code_file': open('tests/cSharp/test-files/Example2.cs', 'rb')}
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
