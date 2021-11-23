import os
import pytest
from app import db
from . import client,auth
from app.go.models_go import GoChallenge
import glob

path='public/challenges*'
def clean():
    path="public/challenges"
    for file in os.listdir(path):
        if (file.endswith(".go")):
            os.remove(os.path.join(path, file))

def test_repair_for_correct_file(client,auth):
    # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                "challenge": { \
                    "source_code_file_name" : "code.go", \
                    "test_suite_file_name" : "code_test.go", \
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
    ret_post = client.post("go/api/v1/go-challenges", data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]

    ret_repair = client.post(f"go/api/v1/go-challenges/{ret_post_json['id']}/repair", data=challenge_repair, headers={'Authorization': f'JWT {auth}'})
    #Assert
    assert ret_repair.status_code == 200

    #cleanup
    clean()

def test_repair_for_incorrect_file(client,auth):
    # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "code2.go", \
                        "test_suite_file_name" : "code2_test.go", \
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
    ret_post = client.post("go/api/v1/go-challenges", data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]

    ret_repair = client.post(f"go/api/v1/go-challenges/{ret_post_json['id']}/repair", data=challenge_repair, headers={'Authorization': f'JWT {auth}'})
    # Assert
    assert ret_repair.status_code == 409

    #cleanup
    clean()

def test_repair_for_not_compile_file(client,auth):
    # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "code3.go", \
                        "test_suite_file_name" : "code3_test.go", \
                        "repair_objective" : "repair", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challenge_repair = {
        'source_code_file': open('tests/go/files-for-tests/median_not_compile.go', 'rb'),
    }

    # Act
    ret_post = client.post("go/api/v1/go-challenges", data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]

    ret_repair = client.post(f"go/api/v1/go-challenges/{ret_post_json['id']}/repair", data=challenge_repair, headers={'Authorization': f'JWT {auth}'})
    # Assert
    assert ret_repair.status_code == 409

    #cleanup
    clean()

def test_repair_for_check_calculate_edit_distance(client,auth):
    # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "code4.go", \
                        "test_suite_file_name" : "code4_test.go", \
                        "repair_objective" : "repair", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challenge_repair = {
        'source_code_file': open('tests/go/files-for-tests/median_solution_3point.go', 'rb'),
    }

    # Act
    ret_post = client.post("go/api/v1/go-challenges", data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]

    ret_repair = client.post(f"go/api/v1/go-challenges/{ret_post_json['id']}/repair", data=challenge_repair, headers={'Authorization': f'JWT {auth}'})
    ret_repair_json = ret_repair.json["repair"]
    assert ret_repair_json["score"] == 3

    #cleanup
    clean()

def test_repair_for_check_upgrade_best_score(client,auth):
    # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "code5.go", \
                        "test_suite_file_name" : "code5_test.go", \
                        "repair_objective" : "repair", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challenge_repair = {
        'source_code_file': open('tests/go/files-for-tests/median_solution_3point.go', 'rb'),
    }

    # Act
    ret_post = client.post("go/api/v1/go-challenges", data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]

    ret_repair = client.post(f"go/api/v1/go-challenges/{ret_post_json['id']}/repair", data=challenge_repair, headers={'Authorization': f'JWT {auth}'})
    ret_repair_json = ret_repair.json["repair"]
    score = ret_repair_json["score"]
    ret_repair_json = ret_repair_json["challenge"]
    # Assert
    assert score == 3
    #Testeo si el bestscore anterior es mayor al actual. Esto se debe cumplir ya que
    #es la primera vez que reparamos el challengue.
    assert ret_post_json["best_score"] > ret_repair_json["best_score"]

    #cleanup
    clean()

def test_repair_for_check_id_not_associated(client,auth):
    # arrange
    challenge_repair = {
        'source_code_file': open('tests/go/files-for-tests/median_solution_3point.go', 'rb'),
    }

    # Act
    ret_repair = client.post("go/api/v1/go-challenges/0/repair", data=challenge_repair, headers={'Authorization': f'JWT {auth}'})
 
    # Assert
    assert ret_repair.status_code == 404

    #cleanup
    clean()