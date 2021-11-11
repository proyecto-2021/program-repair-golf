import os
import pytest
from app import create_app, db
from . import client
from app.go.models_go import GoChallenge
import glob
path='public/challenges*'

def clean():
    path="public/challenges"
    for file in os.listdir(path):
        if not(file.endswith(".md")):
            os.remove(os.path.join(path, file))

def add_new_challenge():
	challenge=GoChallenge(code="tests/go/files-for-tests/median.go",tests_code="tests/go/files-for-tests/median_test.go",repair_objective="repair",complexity="coplexity",best_score=100)
	db.session.add(challenge)
	db.session.commit()
	return challenge.id

def test_get_all_empty(client):
    # arrange

    # act
    ret_get = client.get("/go/api/v1/go-challenges")
    ret_get_json=ret_get.json["challenges"]
    # downgrade
    for file in glob.glob(os.path.abspath(path)):
        if os.path.isfile(file):
            os.remove(file)
    # assert
    assert (ret_get_json=="not found")
    assert ret_get.status_code == 404

def test_get_all_working(client):
    # arrange
    for i in range(0,3):
        add_new_challenge()
        
    
    # act
    ret_get = client.get("/go/api/v1/go-challenges")
    ret_get_json=ret_get.json["challenges"]
    # assert
    assert len(ret_get_json) == 3
    assert ret_get.status_code == 200

  
def test_post_code_with_error(client):
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
    ret_post = client.post("go/api/v1/go-challenges",data=challenge)
    ret_post_json = ret_post.json["code_file"]
    
    # Assert
    assert ret_post.status_code == 412
    assert ret_post_json=="The code has syntax errors"
    
    #cleanup
    clean()

def test_getId_for_id_correct(client):
    # arrange
    challenge = {
        'source_code_file': open('tests/go/files-for-tests/median.go', 'rb'),
        'test_suite_file': open('tests/go/files-for-tests/median_test.go', 'rb'),
        'challenge': '{ \
                "challenge": { \
                    "source_code_file_name" : "codeGet.go", \
                    "test_suite_file_name" : "codeGet_test.go", \
                    "repair_objective" : "repair", \
                    "complexity" : "100", \
                    "best_score" : 100 \
                } \
            }'
    }

    #act
    ret_post = client.post("go/api/v1/go-challenges",data=challenge)
    ret_post_json = ret_post.json["challenge"]
    ret_get = client.get(f"/go/api/v1/go-challenges/{ret_post_json['id']}")
    ret_get_json = ret_get.json["challenge"]

    #assert
    assert ret_get.status_code == 200
    assert ret_get_json["repair_objective"] == ret_post_json["repair_objective"]
    assert ret_get_json["complexity"] == ret_post_json["complexity"]
    assert ret_get_json["best_score"] == ret_post_json["best_score"]

    #cleanup
    clean()

@pytest.mark.parametrize("id", [0, 'string'])
def test_getId_for_id_incorrect(client,id):
    #Arrange

    #Act
    ret = client.get(f'/go/api/v1/go-challenges/{id}')

    #assert
    assert ret.status_code == 404

def test_repair_for_correct_file(client):
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
    ret_post = client.post("go/api/v1/go-challenges", data=challenge)
    ret_post_json = ret_post.json["challenge"]

    ret_repair = client.post(f"go/api/v1/go-challenges/{ret_post_json['id']}/repair", data=challenge_repair)
    #Assert
    assert ret_repair.status_code == 200

    #cleanup
    clean()

def test_repair_for_incorrect_file(client):
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
    ret_post = client.post("go/api/v1/go-challenges", data=challenge)
    ret_post_json = ret_post.json["challenge"]

    ret_repair = client.post(f"go/api/v1/go-challenges/{ret_post_json['id']}/repair", data=challenge_repair)
    # downgrade
    for file in glob.glob(os.path.abspath(path)):
        if os.path.isfile(file):
            os.remove(file)
    # Assert
    assert ret_repair.status_code == 409

    #cleanup
    clean()

def test_repair_for_not_compile_file(client):
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
    ret_post = client.post("go/api/v1/go-challenges", data=challenge)
    ret_post_json = ret_post.json["challenge"]

    ret_repair = client.post(f"go/api/v1/go-challenges/{ret_post_json['id']}/repair", data=challenge_repair)
    # Assert
    assert ret_repair.status_code == 409

    #cleanup
    clean()

def test_repair_for_check_calculate_edit_distance(client):
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
    ret_post = client.post("go/api/v1/go-challenges", data=challenge)
    ret_post_json = ret_post.json["challenge"]

    ret_repair = client.post(f"go/api/v1/go-challenges/{ret_post_json['id']}/repair", data=challenge_repair)
    ret_repair_json = ret_repair.json["repair"]
    # downgrade
    for file in glob.glob(os.path.abspath(path)):
        if os.path.isfile(file):
            os.remove(file)
    # Assert
    assert ret_repair_json["score"] == 3

    #cleanup
    clean()

def test_repair_for_check_upgrade_best_score(client):
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
    ret_post = client.post("go/api/v1/go-challenges", data=challenge)
    ret_post_json = ret_post.json["challenge"]

    ret_repair = client.post(f"go/api/v1/go-challenges/{ret_post_json['id']}/repair", data=challenge_repair)
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

def test_repair_for_check_id_not_associated(client):
    # arrange
    challenge_repair = {
        'source_code_file': open('tests/go/files-for-tests/median_solution_3point.go', 'rb'),
    }

    # Act
    ret_repair = client.post("go/api/v1/go-challenges/0/repair", data=challenge_repair)
 
    # Assert
    assert ret_repair.status_code == 404

    #cleanup
    clean()
