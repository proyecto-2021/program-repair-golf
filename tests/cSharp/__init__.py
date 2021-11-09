from app import create_app, db
import pytest
import shutil, glob

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
        
    #for dir_name in glob.glob('/example-challenges/c-sharp-challenges'):
        #if 'Median' not in dir_name: 
           # shutil.rmtree(dir_name)

