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

def test_update_code_without_codename(client,auth):
     # arrange
    challengeupdate= {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "complexity" : "100" \
                    } \
                }'
    }

    # act
    ret_update = client.put(f"go/api/v1/go-challenges/1", data=challengeupdate, headers={'Authorization': f'JWT {auth}'})
    ret_update_json=ret_update.json["source_code_file_name"]
    
    # assert
    assert ret_update_json=="not found"
    assert ret_update.status_code== 409

    # cleanup

def test_update_test_without_testname(client,auth):
     # arrange
    challengeupdate= {
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "complexity" : "100" \
                    } \
                }'
    }

    # act
    ret_update = client.put(f"go/api/v1/go-challenges/1", data=challengeupdate, headers={'Authorization': f'JWT {auth}'})
    ret_update_json=ret_update.json["test_suite_file_name"]
    
    # assert
    assert ret_update_json=="not found"
    assert ret_update.status_code== 409

    # cleanup

def test_update_id_error(client,auth):
    # arrange
    id=-1
    # act
    ret_update = client.put(f"go/api/v1/go-challenges/-1", headers={'Authorization': f'JWT {auth}'})
    ret_update_json=ret_update.json["challenge"]
    # assert
    assert ret_update_json=="not found"
    assert ret_update.status_code==404

    # cleanup
    clean()
  
def test_update_code_complexity(client,auth):
     # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "codecomplexity.go", \
                        "test_suite_file_name" : "code7complexity_test.go", \
                        "repair_objective" : "without error", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challengeupdate= {
        'challenge': '{ \
                    "challenge": { \
                        "complexity" : "99" \
                    } \
                }'
    }
    # act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]
    postid=ret_post_json["id"]
    ret_update = client.put(f"go/api/v1/go-challenges/{postid}", data=challengeupdate, headers={'Authorization': f'JWT {auth}'})
    ret_update_json=ret_update.json["challenge"]
    
    # assert
    assert ret_update_json["complexity"]=="99"
    assert ret_post.status_code== 200

    # cleanup
    clean()

def test_update_code_repairobj(client,auth):
     # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "coderepair.go", \
                        "test_suite_file_name" : "code7repair_test.go", \
                        "repair_objective" : "without error", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challengeupdate= {
        'challenge': '{ \
                    "challenge": { \
                        "repair_objective" : "testing" \
                    } \
                }'
    }

     # act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]
    postid=ret_post_json["id"]
    ret_update = client.put(f"go/api/v1/go-challenges/{postid}", data=challengeupdate, headers={'Authorization': f'JWT {auth}'})
    ret_update_json=ret_update.json["challenge"]
    
    # assert
    assert ret_update_json["repair_objective"]=="testing"
    assert ret_post.status_code== 200

    # cleanup
    clean()

def test_update_code_with_syntax_error(client,auth):
     # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "codesintaxys.go", \
                        "test_suite_file_name" : "codesintaxys_test.go", \
                        "repair_objective" : "without error", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challengeupdate = {
        'source_code_file': open('tests/go/files-for-tests/median_not_compile.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "codesintaxys.go", \
                        "test_suite_file_name" : "codesintaxys_test.go" \
                    } \
                }'
    }
    # act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]
    postid=ret_post_json["id"]
    ret_update = client.put(f"go/api/v1/go-challenges/{postid}", data=challengeupdate, headers={'Authorization': f'JWT {auth}'})
    ret_update_json = ret_update.json["source_code_file"]
    
    assert ret_update_json=="source code with sintax errors"
    assert ret_update.status_code== 409

    # cleanup
    clean()

def test_update_test_code_with_syntax_error(client,auth):
     # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "codesintaxystest.go", \
                        "test_suite_file_name" : "codesintaxystest_test.go", \
                        "repair_objective" : "without error", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challengeupdate = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_not_compile_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "codesintaxystest.go", \
                        "test_suite_file_name" : "codesintaxystest_test.go" \
                    } \
                }'
    }
    # act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]
    postid=ret_post_json["id"]
    ret_update = client.put(f"go/api/v1/go-challenges/{postid}", data=challengeupdate, headers={'Authorization': f'JWT {auth}'})
    ret_update_json=ret_update.json["test_suite_file"]
    
    # assert
    assert ret_update_json=="tests with sintax errors"
    assert ret_update.status_code== 409

    # cleanup
    clean()

def test_update_with_a_passing_test(client,auth):
     # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "codepassingtestput.go", \
                        "test_suite_file_name" : "codepassingtestput_test.go", \
                        "repair_objective" : "without error", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challengeupdate = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/medianpassing_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "codepassingtestput.go", \
                        "test_suite_file_name" : "codepassingtestput_test.go" \
                    } \
                }'
    }
    # act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]
    postid=ret_post_json["id"]
    ret_update = client.put(f"go/api/v1/go-challenges/{postid}", data=challengeupdate, headers={'Authorization': f'JWT {auth}'})
    ret_update_json=ret_update.json["error"]
    
    # assert
    assert ret_update_json=="tests must fails"
    assert ret_update.status_code== 412

    # cleanup
    clean()

def test_update_code_with_a_passing_test(client,auth):
     # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "codepassingtestputcode.go", \
                        "test_suite_file_name" : "codepassingtestputcode_test.go", \
                        "repair_objective" : "without error", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challengeupdate = {
        'source_code_file': open('tests/go/files-for-tests/median_solution_3point.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "codepassingtestput.go" \
                    } \
                }'
    }
    # act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]
    postid=ret_post_json["id"]
    ret_update = client.put(f"go/api/v1/go-challenges/{postid}", data=challengeupdate, headers={'Authorization': f'JWT {auth}'})
    ret_update_json=ret_update.json["error"]
    
    # assert
    assert ret_update_json=="source code must fails tests"
    assert ret_update.status_code== 412

    # cleanup
    clean()

def test_update_test_with_a_passing_test(client,auth):
     # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "codepassingtestputtest.go", \
                        "test_suite_file_name" : "codepassingtestputtest_test.go", \
                        "repair_objective" : "without error", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challengeupdate = {
        'test_suite_file': open('tests/go/files-for-tests/medianpassing_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "test_suite_file_name" : "codepassingtestput_test.go" \
                    } \
                }'
    }
    # act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]
    postid=ret_post_json["id"]
    ret_update = client.put(f"go/api/v1/go-challenges/{postid}", data=challengeupdate, headers={'Authorization': f'JWT {auth}'})
    ret_update_json=ret_update.json["error"]
    
    # assert
    assert ret_update_json=="tests must fails"
    assert ret_update.status_code== 412

    # cleanup
    clean()

def test_update_test_suite_code(client, auth):
     # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "updatingtestcode.go", \
                        "test_suite_file_name" : "updatingtestcode_test.go", \
                        "repair_objective" : "without error", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challengeupdate = {
        'test_suite_file': open('tests/go/files-for-tests/median2_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "test_suite_file_name" : "median2_test.go" \
                    } \
                }'
    }
    # act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]
    postid=ret_post_json["id"]
    ret_update = client.put(f"go/api/v1/go-challenges/{postid}", data=challengeupdate, headers={'Authorization': f'JWT {auth}'})
    ret_get = client.get(f"/go/api/v1/go-challenges/{postid}", headers={'Authorization': f'JWT {auth}'})
    ret_get_json=ret_get.json["challenge"]
    
    # assert
    assert ret_post_json["tests_code"]!=ret_get_json["tests_code"]
    assert ret_update.status_code== 200

    # cleanup
    clean()

def test_update_source_code(client, auth):
     # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "updatingsourcecode.go", \
                        "test_suite_file_name" : "updatingsourcecode_test.go", \
                        "repair_objective" : "without error", \
                        "complexity" : "100", \
                        "best_score" : 100 \
                    } \
                }'
    }

    challengeupdate = {
        'source_code_file': open('tests/go/files-for-tests/median2.go', 'rb'),
        'challenge': '{ \
                    "challenge": { \
                        "source_code_file_name" : "median2.go" \
                    } \
                }'
    }
    # act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]
    postid=ret_post_json["id"]
    ret_update = client.put(f"go/api/v1/go-challenges/{postid}", data=challengeupdate, headers={'Authorization': f'JWT {auth}'})
    ret_get = client.get(f"/go/api/v1/go-challenges/{postid}", headers={'Authorization': f'JWT {auth}'})
    ret_get_json=ret_get.json["challenge"]
    
    # assert
    assert ret_post_json["code"]!=ret_get_json["code"]
    assert ret_update.status_code== 200

    # cleanup
    clean()