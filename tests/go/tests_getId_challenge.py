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

def test_getId_for_id_correct(client,auth):
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
    ret_post = client.post("go/api/v1/go-challenges",data=challenge, headers={'Authorization': f'JWT {auth}'})
    ret_post_json = ret_post.json["challenge"]
    ret_get = client.get(f"/go/api/v1/go-challenges/{ret_post_json['id']}", headers={'Authorization': f'JWT {auth}'})
    ret_get_json = ret_get.json["challenge"]

    #assert
    assert ret_get.status_code == 200
    assert ret_get_json["repair_objective"] == ret_post_json["repair_objective"]
    assert ret_get_json["complexity"] == ret_post_json["complexity"]
    assert ret_get_json["best_score"] == ret_post_json["best_score"]

    #cleanup
    clean()

@pytest.mark.parametrize("id", [0, 'string'])
def test_getId_for_id_incorrect(client,id,auth):
    #Arrange

    #Act
    ret = client.get(f'/go/api/v1/go-challenges/{id}', headers={'Authorization': f'JWT {auth}'})

    #assert
    assert ret.status_code == 404