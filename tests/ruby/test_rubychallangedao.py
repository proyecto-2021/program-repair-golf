from . import client
from app.ruby.rubychallengedao import RubyChallengeDAO

def test_create_challenge(client):
    dao = RubyChallengeDAO()
    id = dao.create_challenge("path/to/example.rb","path/to/example_tests.rb","Testing","5")

    assert id is not None