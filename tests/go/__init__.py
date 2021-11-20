from _pytest.config import filename_arg
from app import create_app, db
import pytest
import os
import glob

@pytest.fixture(scope='module')
def client():
    # Arrange
    path='public/challenges'
    app = create_app('testing')
    # Create a test client using the Flask application configured for testing
    with app.test_client() as test_client:
        # Establish an application context
        with app.app_context():
            db.create_all()
            # Tests will be executed on the test_client object
            yield test_client
            
    #Cleanup
    for file in os.listdir(path):
        if (file.endswith(".go")):
            os.remove(os.path.join(path, file))
   
       
@pytest.fixture(scope='module')
def auth(client):
    user = {'username': 'user', 'password': 'root'}
    
    ret_post_user = client.post("/users", json=user)
    ret_post_auth = client.post("/auth", json=user)
    
    acces_token = ret_post_auth.json["access_token"]
    
    return acces_token