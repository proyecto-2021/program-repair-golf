import os
import pytest
from app import create_app, db
from . import client
from app.go.models_go import GoChallenge


def test_getId_for_id_correct(client):
    # arrange
    challengue = GoChallenge(code="code_path", tests_code="test_path", repair_objective="repair", complexity="1",
                             best_score=100)

    #act
    ret_pos = client.post("/api/v1/go-challenges",json=challengue)
    ret_get = client.get(f"/api/v1/go-challenges/{ret_pos.json()['id']}")

    #assert
    ret_pos_json = ret_pos.json()
    ret_get_json = ret_get.json()

    assert ret_get.status_code == 200
    assert ret_get_json.json()["id"] == ret_pos_json.json()["id"]
    assert ret_get_json.json()["code_path"] == ret_pos_json.json()["code_path"]
    assert ret_get_json.json()["tests_code"] == ret_pos_json.json()["tests_code"]
    assert ret_get_json.json()["repair_objective"] == ret_pos_json.json()["repair_objective"]
    assert ret_get_json.json()["complexity"] == ret_pos_json.json()["complexity"]
    assert ret_get_json.json()["best_score"] == ret_pos_json.json()["best_score"]

