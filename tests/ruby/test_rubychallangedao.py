from . import client
from app.ruby.rubychallengedao import RubyChallengeDAO

def test_create_challenge(client):
    dao = RubyChallengeDAO()
    id = dao.create_challenge('path/to/example.rb', 'path/to/example_tests.rb', 'Testing', '5')

    assert id is not None

def test_get_one_after_create(client):
    dao = RubyChallengeDAO()
    id = dao.create_challenge('path/to/example.rb', 'path/to/example_tests.rb', 'Testing', '5')

    challenge = dao.get_challenge(id)


    assert challenge == {
        'code': 'path/to/example.rb',
        'tests_code': 'path/to/example_tests.rb',
        'repair_objective': 'Testing',
        'best_score':  0,
        'complexity': '5'
    }
