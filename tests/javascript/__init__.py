from app import create_app, db
import pytest

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

@pytest.fixture(scope='module')
def auth(client):
    user = {'username': 'js', 'password': 'js'}
    r = client.post('/users', json=user)
    r = client.post('/auth', json=user)
    token = r.json['access_token']
    return token