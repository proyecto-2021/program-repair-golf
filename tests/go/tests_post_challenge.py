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

def test_post_code_with_error(client,auth):
    # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median_not_compile.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "code6.go", \
                        "test_suite_file_name" : "code6_test.go", \
                        "repair_objective" : "repair", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    # Act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["code_file"]
    
    # Assert
    assert ret_post.status_code == 412
    assert ret_post_json=="The code has syntax errors"
    
    #cleanup
    clean()

def test_post_code_without_error(client,auth):
     # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "code7.go", \
                        "test_suite_file_name" : "code7_test.go", \
                        "repair_objective" : "without error", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    # act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]
    
    # assert
    assert ret_post_json["repair_objective"]=="without error"
    assert ret_post.status_code== 200

    # cleanup
    clean()

def test_post_testscode_with_error(client,auth):
    # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_not_compile_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "code8.go", \
                        "test_suite_file_name" : "code8_test.go", \
                        "repair_objective" : "repair", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    # Act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["test_code_file"]
    # Assert
    assert ret_post_json== "The test code has syntax errors"
    assert ret_post.status_code== 412

    # cleanup
    clean()

def test_post_testscode_with_error(client,auth):
    # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/medianpassing_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "code9.go", \
                        "test_suite_file_name" : "code9_test.go", \
                        "repair_objective" : "repair", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    # Act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["ERROR: tests"]
    # Assert
    assert ret_post_json=="There must be at least one test that fails"
    assert ret_post.status_code== 412

    # cleanup
    clean()

def test_post_repeated(client,auth):
     # arrange
    challenge1 = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb') ,
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "code10.go", \
                        "test_suite_file_name" : "code10_test.go", \
                        "repair_objective" : "repair", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }
    challenge2 = {
        'source_code_file': open('tests/go/files-for-tests/median_solution_3point.go', 'rb') ,
        'test_suite_file': open('tests/go/files-for-tests/median2_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "code10.go", \
                        "test_suite_file_name" : "code10_test.go", \
                        "repair_objective" : "repair", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }


    # act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge1, headers={'Authorization': f'JWT {auth}'})
    ret_post = client.post("go/api/v1/go-challenges",data=challenge2, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]
    
    # assert
    assert ret_post_json=="repeated"
    assert ret_post.status_code == 409

    # cleanup
    clean()