from app import create_app, db
import pytest
from app.go.models_go import GoChallenge
from . import client

def add_new_challenge():
    challenge=GoChallenge(code="path",tests_code="test_path",repair_objective="repair",complexity="coplexity",best_score=100)
    db.session.add(challenge)
    db.session.commit()
    return challenge.id()


def test_get_challenge_go():
    id=add_new_challenge()
    challenge= GoChallenge.query.filter_by(id=id).first()
    assert (challenge is None) == False

