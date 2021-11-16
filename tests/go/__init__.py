from app import create_app, db
import pytest
import os

@pytest.fixture(scope='module')
def client():
    # Arrange
    filename='////tmp'
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
    user = {'username': 'user', 'password': 'root'}
    
    ret_post_user = client.post("/users", json=user)
    ret_post_auth = client.post("/auth", json=user)
    
    acces_token = ret_post_auth.json["access_token"]
    
    return acces_token


    