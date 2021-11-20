import os
import pytest
from app import create_app, db
from . import *
import shutil

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