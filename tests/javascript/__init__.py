from app import create_app, db
import pytest
from app.javascript.controllers.files_controller import open_file

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

#importar open file
def createChallenge( code_name, test_name,objective,complexity):
    code_path = f'example-challenges/javascript-challenges/{code_name}.js'
    test_path = f'example-challenges/javascript-challenges/{test_name}.js'

    challenge = {
		'source_code_file': open_file(code_path),
		'test_suite_file': open_file(test_path),
		f'challenge':'{ \
            "challenge":{\
                "source_code_file_name":{code_name},\
                "test_suite_file_name": {test_name},\
                "repair_objective": {objective} ,\
                "complexity": {complexity}\
            }\
        }'
	}
    return challenge