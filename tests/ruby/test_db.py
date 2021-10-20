from app import create_app, db
import pytest
from app.ruby.models import RubyChallenge
from app.ruby.views import create_challenge

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


def test_add_challenge(client):
    challenge = RubyChallenge(
        code='code',
        tests_code='tests_code',
        repair_objective='repair_objective',
        complexity='5',
        best_score=0
    )

    create_challenge(challenge)

    assert len(RubyChallenge.query.all()) == 1
