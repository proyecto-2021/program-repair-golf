import os
import pytest
from app import create_app, db
from . import client
from app.go.models_go import GoChallenge


def test_getId_for_id_correct(client):
    # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                "challenge": { \
                    "source_code_file_name" : "code", \
                    "test_suite_file_name" : "code_test", \
                    "repair_objective" : "repair", \
                    "complexity" : "100" \
                } \
            }'
    }


    #act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge)
    ret_post_json = ret_post.json["challenge"]
    ret_get = client.get(f"/go/api/v1/go-challenges/{ret_post_json['id']}")
    ret_get_json = ret_get.json["challenge"]

    #assert
    #assert ret_post.status_code == 200

    assert ret_get.status_code == 200
    #assert ret_get_json["code_path"] == ret_post_json["code_path"]
    #assert ret_get_json["tests_code"] == ret_post_json["tests_code"]
    assert ret_get_json["repair_objective"] == ret_post_json["repair_objective"]
    assert ret_get_json["complexity"] == ret_post_json["complexity"]
    assert ret_get_json["best_score"] == ret_post_json["best_score"]
