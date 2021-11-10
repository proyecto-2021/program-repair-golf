from . import client
from app import create_app, db
from app.cSharp.models import *
from app.cSharp.views import *
import pytest


@pytest.fixture
def new_challenge():
    challenge = CSharpChallengeModel(code="./tests/test-files/Example1.cs",
                                     tests_code="./tests/test-files/Example1Test.cs",
                                     repair_objective="testing the db",
                                     complexity=5,
                                     best_score=0)
    db.session.add(challenge)
    db.session.commit()
    return challenge


@pytest.fixture
def expected_challenge(new_challenge):
    return new_challenge.__repr__()


def test_get_challenge_from_db_without_files_contents(client, expected_challenge):
    # Test get_challenge_db method with show_files_content=False
    ch_id = expected_challenge['id']
    challenge_from_get = get_challenge_db(ch_id)
    assert challenge_from_get == expected_challenge
