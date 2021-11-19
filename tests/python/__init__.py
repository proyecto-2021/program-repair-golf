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

    for file in os.listdir("/public/challenges/"):
        if file != 'README':
            os.remove(os.path.join("/public/challenges/", file))
