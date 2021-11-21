from app import create_app, db
import pytest
from app.javascript.controllers.files_controller import open_file, remove_files
from app.javascript.dao.challenge_dao import ChallengeDAO

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


@pytest.fixture(scope='module')
def post_generator(client, auth):
    data = createChallenge('example0', 'example0.test', 'Testing', '1')
    r = client.post('javascript/javascript-challenges', data=data, headers={'Authorization': f'JWT {auth}'})
    return r.json

#importar open file
def createChallenge( code_name, test_name,objective,complexity):
    code_path = f'example-challenges/javascript-challenges/{code_name}.js'
    test_path = f'example-challenges/javascript-challenges/{test_name}.js'
    
    challenge = {
		'source_code_file': open(code_path, 'rb'),
		'test_suite_file': open(test_path, 'rb'),
		'challenge':'{ \
            "challenge":{\
                "source_code_file_name": "median",\
                "test_suite_file_name": "median.test",\
                "repair_objective": "objective",\
                "complexity": "number"\
            }\
        }'
	}

    challenge['challenge'] = challenge['challenge'].replace('median', code_name)
    challenge['challenge'] = challenge['challenge'].replace('median.test', test_name)
    challenge['challenge'] = challenge['challenge'].replace('objetive', objective)
    challenge['challenge'] = challenge['challenge'].replace('number', complexity)


    return challenge

