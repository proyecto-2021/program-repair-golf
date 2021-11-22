from . import client


def test_insert_admin_user(client):
    # arrange
    user_dict = {'username': 'admin', 'password': 'admin'}
    # act
    r = client.post('/users', json=user_dict)
    # assert
    assert r.status_code == 200
    assert r.json == {'id': 1, 'username': 'admin'}


def test_insert_admin_user_twice(client):
    # arrange
    user_dict = {'username': 'user', 'password': 'user'}
    # act
    client.post('/users', json=user_dict)
    r = client.post('/users', json=user_dict)
    # assert
    assert r.status_code == 400
