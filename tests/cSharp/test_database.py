from . import client
from app.cSharp.models import *
import pytest


@pytest.fixture
def new_challenge():
    challenge = CSharpChallengeModel(code="./tests/cSharp/test-files/BaseExample.cs",
                                     tests_code="./tests/cSharp/test-files/BaseTest.cs",
                                     repair_objective="testing the db",
                                     complexity=5,
                                     best_score=0)
    db.session.add(challenge)
    db.session.commit()
    return challenge


@pytest.fixture
def expected_challenge(new_challenge):
    return new_challenge.__repr__()


@pytest.fixture
def expected_challenge_w_f_contents(new_challenge):
    challenge = new_challenge.__repr__()
    with open('tests/cSharp/test-files/BaseExample.cs') as f:
        challenge['code'] = f.read()
    with open('tests/cSharp/test-files/BaseTest.cs') as f:
        challenge['tests_code'] = f.read()
    return challenge


def test_get_challenge_from_db_without_files_contents(client, expected_challenge):
    # Test get_challenge_db method with show_files_content=False
    ch_id = expected_challenge['id']
    challenge_from_get = get_challenge_db(ch_id)
    assert challenge_from_get == expected_challenge

    # Cleanup
    db.session.query(CSharpChallengeModel).delete()


def test_get_challenge_from_db_with_files_contents(client, expected_challenge_w_f_contents):
    ch_id = expected_challenge_w_f_contents['id']
    challenge_from_get = get_challenge_db(ch_id, show_files_content=True)
    assert challenge_from_get == expected_challenge_w_f_contents

    # Cleanup
    db.session.query(CSharpChallengeModel).delete()

def test_exist(client, expected_challenge):
    # Arrange
    ch_id = expected_challenge['id']

    # Act 
    result_true = exist(ch_id)
    result_false = exist(ch_id + 1)

    #Assert
    assert result_true
    assert not result_false

    # Cleanup
    db.session.query(CSharpChallengeModel).delete() 

def test_update(client, expected_challenge):
    # TODO 
    pass