from app import create_app, db
from app.auth.usermodel import User
import pytest
import os, glob

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

    for filename in glob.glob('/tmp/example*'):
        os.remove(filename)


@pytest.fixture(scope='module')
def auth(client):
    user = {'username': 'ruby', 'password': 'ruby'}
    r = client.post('/users', json=user)
    r = client.post('/auth', json=user)
    token = r.json['access_token']
    return token