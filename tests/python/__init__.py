import pytest
from app import create_app, db
import os

@pytest.fixture(scope = 'module')
def client():
    #arrange
    app = create_app('testing')
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        # Establish an application context
        with app.app_context():
            db.create_all()
            # test will be executed on the test_client object
            yield test_client

    #get path where challenges are stored
    public_path = "public/challenges/"
    public_path = os.path.abspath(public_path)
    #delete all challenges
    for file in os.listdir(public_path):
        print(f"\n{file}")
        if file != 'README.md': #don't delete readme
            os.remove(os.path.join(public_path, file))

@pytest.fixture(scope = 'module')
def jwt_token(client):
    #creating the user
    user = {'username': 'el gran pepito', 'password': 'user'}
    client.post('/users', json=user)
    auth_result = client.post('/auth', json=user)
    #getting a token
    return auth_result.json['access_token']
