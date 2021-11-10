from app import create_app, db
import pytest


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


def test_insert_admin_user(client):
    # arrange
    user_dict = {'username': 'admin', 'password': 'admin'}
    # act
    r = client.post('/users/', json=user_dict)
    # assert
    assert r.status_code == 200
    assert r.json == {'id': 1, 'username': 'admin'}


def test_insert_admin_user_twice(client):
    # arrange
    user_dict = {'username': 'user', 'password': 'user'}
    # act
    client.post('/users/', json=user_dict)
    r = client.post('/users/', json=user_dict)
    # assert
    assert r.status_code == 400
