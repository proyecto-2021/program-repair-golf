from . import client
from .data_generator import get_data

def test_get_after_post(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data('example2', 'example_test2', 'Testing', '5', 'example_challenge', 'example_test2')
    r = client.post(url, data=data)
    id = r.json['challenge']['id']
    post_result = r.json['challenge']
    post_result.pop('id')
    url2 = f'/ruby/challenge/{id}'

    #act
    r2 = client.get(url2)

    #assert
    assert r.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] == post_result

def test_get_invalid_challenge(client):
    #arrange
    url = '/ruby/challenge/1000'

    #act
    r = client.get(url)

    #assert
    assert r.status_code == 404
    assert r.json['challenge'] == 'the id does not exist'

def test_get_all_after_post(client):
    #arrange
    url = '/ruby/challenges'
    r1 = client.get(url)
    list1 = r1.json['challenges']
    url = '/ruby/challenge'
    data = get_data('example21', 'example_test21', 'Testing', '4', 'example_challenge', 'example_test21')
    r2 = client.post(url, data=data)
    post_result = r2.json['challenge']
    post_result.pop('tests_code')
    url2 = '/ruby/challenges'

    #act
    r3 = client.get(url2)
    list2 = r3.json['challenges']

    #assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r3.status_code == 200
    assert len(list1) == len(list2) - 1
    assert set(challenge['id'] for challenge in list1).issubset(set(challenge['id'] for challenge in list2))
    assert post_result in list2