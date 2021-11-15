from . import client
from .data_generator import get_data

def test_get_after_post(client):
    url = '/ruby/challenge'
    data = get_data('example2', 'example_test2', 'Testing', '5', 'example_challenge', 'example_test2')

    r = client.post(url, data=data)
    json = r.json['challenge']
    id = json['id']
    del json['id']

    url2 = f'/ruby/challenge/{id}'
    r2 = client.get(url2)
    json2 = r2.json['challenge']

    assert r.status_code == 200
    assert r2.status_code == 200
    assert json == json2

def test_get_invalid_challenge(client):
    url = '/ruby/challenge/1000'

    r = client.get(url)

    assert r.status_code == 404
    assert r.json['challenge'] == 'id doesnt exist'

def test_get_all_after_post(client):
    url = '/ruby/challenges'
    r = client.get(url)
    list1 = r.json['challenges']

    url = '/ruby/challenge'
    data = get_data('example3', 'example_test3', 'Testing', '4', 'example_challenge', 'example_test3')

    r2 = client.post(url, data=data)

    url = '/ruby/challenges'
    r3 = client.get(url)
    list2 = r3.json['challenges']

    assert r.status_code == 200
    assert r2.status_code == 200
    assert r3.status_code == 200
    assert len(list1) == len(list2) - 1

def test_get_all_after_post2(client):
    url = '/ruby/challenge'
    data = get_data('example21', 'example_test21', 'Testing', '4', 'example_challenge', 'example_test21')
    r = client.post(url, data=data)

    json = r.json['challenge']
    del json['tests_code']

    url = '/ruby/challenges'
    r2 = client.get(url)
    list = r2.json['challenges']

    assert r.status_code == 200
    assert r2.status_code == 200
    assert json in list
