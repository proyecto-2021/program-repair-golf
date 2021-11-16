from app import create_app, db
import pytest
import os
import shutil
from app.cSharp.models import CSharpChallengeModel

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
    cleanup_dirs()

@pytest.fixture
def create_test_data():
    data = create_challenge('Example1', 'Example1Test', 'Testing', '5', 'BaseExample', 'BaseTest')

    with open('tests/cSharp/test-files/BaseExample.cs') as f:
        content_code = f.read()
    with open('tests/cSharp/test-files/BaseTest.cs') as f:
        content_tests_code = f.read()

    return {'data': data,
            'content_code': content_code,
            'content_tests_code': content_tests_code
            }

def challenge_json(dic_data):
    json_dic = '{ "challenge": { '
    if dic_data[next(iter(dic_data))] is not None:
        first_key = list(dic_data)[0]
    for key in dic_data:
        if dic_data[key] is not None:
            if key == first_key:
                json_dic += f'"{key}" : "{dic_data[key]}"'
            else:
                json_dic += f', "{key}" : "{dic_data[key]}"'

    json_dic += ' } }'
    return {'challenge': json_dic}

def create_challenge(code_name=None, tests_name=None, repair_objective=None, complexity=None, code=None, tests_code=None):
    challenge = {}
    if code is not None:
        challenge.update({'source_code_file': open(f'tests/cSharp/test-files/{code}.cs', 'rb')})
    if tests_code is not None:
        challenge.update({'test_suite_file': open(f'tests/cSharp/test-files/{tests_code}.cs', 'rb')})

    dict_data = {'source_code_file_name': code_name,
                 'test_suite_file_name': tests_name,
                 'repair_objective': repair_objective,
                 'complexity': complexity}

    challenge.update(challenge_json(dict_data))
    return challenge

def cleanup():
    db.session.query(CSharpChallengeModel).delete()
    path = "./example-challenges/c-sharp-challenges"
    for dirname in os.listdir(path):
        if os.path.isdir(path + '/' + dirname) and dirname != "Median":
            shutil.rmtree(path + '/' + dirname)

def cleanup_dirs():
    path = "./example-challenges/c-sharp-challenges"
    for dirname in os.listdir(path):
        if os.path.isdir(path + '/' + dirname) and dirname != "Median":
            shutil.rmtree(path + '/' + dirname)
