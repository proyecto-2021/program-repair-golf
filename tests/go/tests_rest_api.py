import os
import pytest
from app import create_app, db
from . import client
from app.go.models_go import GoChallenge

def test_repair_for_correct_file(client):
    # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                "challenge": { \
                    "source_code_file_name" : "code", \
                    "test_suite_file_name" : "code_test", \
                    "repair_objective" : "repair", \
                    "complexity" : "100", \
                    "best_score" : 100 \
                } \
            }'
    }

    challenge_repair = {
        'source_code_file': open('tests/go/files-for-tests/median_solution_3point.go', 'rb'),
    }

    #Act
    ret_post = client.post("go/api/v1/go-challenges", data=challenge)
    ret_post_json = ret_post.json["challenge"]

    ret_repair = client.post(f"go/api/v1/go-challenges/{ret_post_json['id']}/repair", data=challenge_repair)

    #Assert

    assert ret_repair.status_code == 200

def test_repair_for_incorrect_file(client):
    # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "code", \
                        "test_suite_file_name" : "code_test", \
                        "repair_objective" : "repair", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challenge_repair = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
    }

    # Act
    ret_post = client.post("go/api/v1/go-challenges", data=challenge)
    ret_post_json = ret_post.json["challenge"]

    ret_repair = client.post(f"go/api/v1/go-challenges/{ret_post_json['id']}/repair", data=challenge_repair)

    # Assert

    assert ret_repair.status_code == 409

