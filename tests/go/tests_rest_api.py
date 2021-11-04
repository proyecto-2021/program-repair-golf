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
    ret_get = client.get(f"/api/v1/go-challenges/{ret_pos.json().id}")

    #assert
    assert ret_get.status_code == 200
    assert ret_get.json.id == ret_pos.json.id


