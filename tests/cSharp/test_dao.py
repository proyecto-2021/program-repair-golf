from . import client
from app import db
from app.cSharp.models import CSharpChallengeModel
from app.cSharp.c_sharp_challenge_DAO import CSharpChallengeDAO
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
    dao = CSharpChallengeDAO()
    ch_id = expected_challenge['id']
    challenge_from_get = dao.get_challenge_db(ch_id)
    assert challenge_from_get == expected_challenge

    # Cleanup
    db.session.query(CSharpChallengeModel).delete()


def test_get_challenge_from_db_with_files_contents(client, expected_challenge_w_f_contents):
    dao = CSharpChallengeDAO()
    ch_id = expected_challenge_w_f_contents['id']
    challenge_from_get = dao.get_challenge_db(ch_id, show_files_content=True)
    assert challenge_from_get == expected_challenge_w_f_contents

    # Cleanup
    db.session.query(CSharpChallengeModel).delete()

def test_exist(client, expected_challenge):
    # Arrange
    dao = CSharpChallengeDAO()
    ch_id = expected_challenge['id']

    # Act 
    result_true = dao.exist(ch_id)
    result_false = dao.exist(ch_id + 1)

    #Assert
    assert result_true
    assert not result_false

    # Cleanup
    db.session.query(CSharpChallengeModel).delete() 

def test_update(client, expected_challenge):
    # Arrange
    dao = CSharpChallengeDAO()
    ch_id = expected_challenge['id']
    data = {"complexity":2}
    
    #Act
    dao.update_challenge_data(ch_id, data)
    ch_updated = db.session.query(CSharpChallengeModel).filter_by(id=ch_id).first().__repr__()

    #Assert
    assert ch_updated["complexity"] == data["complexity"]

    # Cleanup
    db.session.query(CSharpChallengeModel).delete()   

def test_remove(client):
    #Arrange
    path1 = "./tests/cSharp/test-files/remove_example" 

    #Act
    dao.remove(path1)

    #Assert
    assert os.path.exists(path1) 

