from . import client


def test_unauthorized_get_access(client):
    # arrange
    # act
    r = client.get('/users')
    # assert
    assert r.status_code == 401
    assert r.json['error'] == "Authorization Required"


def test_authorized_get_access(client):
    # arrange
    user_dict = {'username': 'user', 'password': 'user'}
    # act
    r = client.post('/users', json=user_dict)

    r = client.post('/auth', json=user_dict)
    token = r.json['access_token']

    r = client.get('/users', headers={'Authorization': f'JWT {token}'})
    res_list = r.json
    # assert
    assert r.status_code == 200
    assert len(res_list) == 1
    assert res_list[0]['username'] == 'user'


def test_get_non_existent_user_authorization_error(client):
    # arrange
    user_dict = {'username': 'another_user', 'password': 'another_user'}
    # act
    r = client.post('/auth', json=user_dict)
    # assert
    assert r.status_code == 401
    assert r.json['error'] == "Bad Request"
    assert r.json['description'] == "Invalid credentials"
    assert 'access_token' not in r.json.keys()


def test_get_bad_password_authorization_error(client):
    # arrange
    user_dict = {'username': 'another_user', 'password': 'another_user'}
    # act
    r = client.post('/users', json=user_dict)

    user_dict = {'username': 'another_user', 'password': 'wrong'}
    r = client.post('/auth', json=user_dict)
    # assert
    assert r.status_code == 401
    assert r.json['error'] == "Bad Request"
    assert r.json['description'] == "Invalid credentials"
    assert 'access_token' not in r.json.keys()



