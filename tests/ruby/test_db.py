from app import create_app, db
import pytest
from app.ruby.models import RubyChallenge

@pytest.fixture(scope='module')
def client():
    # Arrange
    app = create_app('testing')
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        # Establish an application context
        with app.app_context():
            db.create_all()
            # Tests will be executed on the test_client object
            yield test_client

            # Cleanup
            # FIXME: Pablo: I guess this is not needed for an in-memory DB?
            # db.drop_all()


def generate_challenge():
    challenge = RubyChallenge(
        code='code',
        tests_code='tests_code',
        repair_objective='repair_objective',
        complexity='5',
        best_score=0
    )
    
    return challenge

def test_create_challenge(client):
    challenge = generate_challenge()
    RubyChallenge.create_challenge(challenge)

    assert len(RubyChallenge.query.all()) == 1

def test_get_challenge(client):
    challenge1 = RubyChallenge.get_challenge(1)
    RubyChallenge.create_challenge(generate_challenge())
    challenge2 = RubyChallenge.get_challenge(2)

    assert challenge1.get_dict()['id'] == 1
    assert challenge2.get_dict()['id'] == 2

