import os
import pytest
from app import create_app, db
from . import *
from app.cSharp.models import CSharpChallengeModel
import shutil


def test_post_repair(client, create_test_data, auth):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair = {'source_code_file': open('tests/cSharp/test-files/ExampleNoFails.cs', 'rb')}
    
    expected_response = {'Repair': { 'challenge':{
                                                'repair_objective': 'Testing',
                                                'best_score': 2 
                                                },
                                    'player':{
                                            'username': "cSharp"
                                            },
                                    'attempts': 1, 
                                    'score': 2
                                    }
                        }
    
    #Act
    resp_post = client.post(url_post, data=data, headers={'Authorization': f'JWT {auth}'})
    challenge_id = resp_post.json['challenge']['id'] 

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair = client.post(url_repair, data=data_repair, headers={'Authorization': f'JWT {auth}'})

    #Assert
    assert resp_repair.status_code == 200
    assert resp_repair.json == expected_response
    #CleanUp
    cleanup()

def test_repair_code_w_sintax_error(client, create_test_data, auth):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair = {'source_code_file': open('tests/cSharp/test-files/ExampleSintaxErrors.cs', 'rb')}
    expected_response = {'Repair candidate': 'Sintax error'}

    #Act
    resp_post = client.post(url_post, data=data, headers={'Authorization': f'JWT {auth}'})
    challenge_id = resp_post.json['challenge']['id'] 

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair = client.post(url_repair, data=data_repair, headers={'Authorization': f'JWT {auth}'})

    #Assert
    assert resp_repair.status_code == 409
    assert resp_repair.json == expected_response
    #CleanUp
    cleanup()


def test_repair_challenge_id_not_exist(client, create_test_data, auth):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair = {'source_code_file': open('tests/cSharp/test-files/ExampleNoFails.cs', 'rb')}
    expected_response = {"challenge": "There is no challenge for this id"}
    #Act
    resp_post = client.post(url_post, data=data, headers={'Authorization': f'JWT {auth}'})
    challenge_id = resp_post.json['challenge']['id'] + 1 

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair = client.post(url_repair, data=data_repair, headers={'Authorization': f'JWT {auth}'})

    #Assert
    assert resp_repair.status_code == 404
    assert resp_repair.json == expected_response
    #CleanUp
    cleanup()


def test_repair_fails_tests(client, create_test_data, auth):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair = {'source_code_file': open('tests/cSharp/test-files/BaseExample.cs', 'rb')}
    expected_response = {'Repair candidate': 'Tests not passed'}

    #Act
    resp_post = client.post(url_post, data=data, headers={'Authorization': f'JWT {auth}'})
    challenge_id = resp_post.json['challenge']['id']

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair = client.post(url_repair, data=data_repair, headers={'Authorization': f'JWT {auth}'})

    #Assert
    assert resp_repair.status_code == 409
    assert resp_repair.json == expected_response

    #CleanUp
    cleanup()


def test_repair_no_file_in_request(client, create_test_data, auth):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair = {}
    expected_response = {'Repair candidate': 'Not found'}

    #Act
    resp_post = client.post(url_post, data=data, headers={'Authorization': f'JWT {auth}'})
    challenge_id = resp_post.json['challenge']['id']

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair = client.post(url_repair, data=data_repair, headers={'Authorization': f'JWT {auth}'})

    #Assert
    assert resp_repair.status_code == 404
    assert resp_repair.json == expected_response

    #CleanUp
    cleanup()


def test_post_better_repair(client, create_test_data, auth):
    #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair_1 = {'source_code_file': open('tests/cSharp/test-files/ExampleNoFails.cs', 'rb')}
    data_repair_2 = {'source_code_file': open('tests/cSharp/test-files/ExampleNoFailsLonger.cs', 'rb')}

    #Act
    resp_post = client.post(url_post, data=data, headers={'Authorization': f'JWT {auth}'})
    challenge_id = resp_post.json['challenge']['id']

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair_1 = client.post(url_repair, data=data_repair_1, headers={'Authorization': f'JWT {auth}'})
    resp_repair_2 = client.post(url_repair, data=data_repair_2, headers={'Authorization': f'JWT {auth}'})

    #Assert
    assert resp_repair_1.json['Repair']['challenge']['best_score'] == resp_repair_2.json['Repair']['challenge']['best_score']
    assert resp_repair_1.json['Repair']['score'] < resp_repair_2.json['Repair']['score']
    assert resp_repair_2.json['Repair']['attempts'] == resp_repair_1.json['Repair']['attempts']+1

    #CleanUp
    cleanup()


def test_diferent_code_repair_to_test(client, create_test_data, auth):
     #Arrange
    url_post = 'cSharp/c-sharp-challenges'
    data = create_test_data['data']
    data_repair = {'source_code_file': open('tests/cSharp/test-files/ExampleNoFails2.cs', 'rb')}
    expected_response = {'Repair candidate': 'Sintax error'}

    #Act
    resp_post = client.post(url_post, data=data, headers={'Authorization': f'JWT {auth}'})
    challenge_id = resp_post.json['challenge']['id']

    url_repair = 'cSharp/c-sharp-challenges/' + str(challenge_id) + '/repair'
    resp_repair = client.post(url_repair, data=data_repair, headers={'Authorization': f'JWT {auth}'})

    #Assert
    assert resp_repair.status_code == 409
    assert resp_repair.json == expected_response

    #CleanUp
    cleanup()