from app import create_app, db
from .data_generator import get_data
import pytest
import os
import glob


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
    for filename in glob.glob('/tmp/new_example*'):
        os.remove(filename)


@pytest.fixture(scope='module')
def auth(client):
    user = {'username': 'ruby', 'password': 'ruby'}
    client.post('/users', json=user)
    r = client.post('/auth', json=user)
    token = r.json['access_token']
    return token


@pytest.fixture(scope='module')
def generic_post(client, auth):
    data = get_data('example', 'example_test', 'Testing', '1', 'example', 'example_test')
    r = client.post('ruby/challenge', data=data, headers={'Authorization': f'JWT {auth}'})
    return r.json
