from . import client
from app import create_app, db
from app.cSharp.models import *
from app.cSharp.views import *
import pytest


def test_get_challenge_from_db_without_files_contents(client):
    # Test get_challenge_db method with show_files_content=False
    challenge = CSharpChallengeModel(code="test-code-path",
                                     tests_code="test-test-path",
                                     repair_objective="testing the db",
                                     complexity=5,
                                     best_score=0)
    db.session.add(challenge)
    db.session.commit()
    ch_id = challenge.id
    ch_dict = challenge.__repr__()
    challenge_from_get = get_challenge_db(ch_id)
    assert challenge_from_get == ch_dict
