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
        if not(file.endswith(".md")):
            os.remove(os.path.join(path, file))
            
    