from . import client, auth, generic_post
from .data_generator import get_data


def test_get_after_post(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    orig_json.pop('id')
    url = f'/ruby/challenge/{challenge_id}'

    # act
    r = client.get(url, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 200
    assert r.json['challenge'] == orig_json


def test_get_invalid_challenge(client, auth):
    # arrange
    url = '/ruby/challenge/1000'

    # act
    r = client.get(url, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 404
    assert r.json['challenge'] == 'the id does not exist'


def test_get_all_after_post(client, auth):
    # arrange
    url1 = '/ruby/challenges'
    r1 = client.get(url1, headers={'Authorization': f'JWT {auth}'})
    list1 = r1.json['challenges']
    url2 = '/ruby/challenge'
    data = get_data('example3', 'example_test3', 'Testing', '4', 'example', 'example_test3')
    r2 = client.post(url2, data=data, headers={'Authorization': f'JWT {auth}'})
    post_result = r2.json['challenge']
    post_result.pop('tests_code')

    # act
    r3 = client.get(url1, headers={'Authorization': f'JWT {auth}'})
    list2 = r3.json['challenges']

    # assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r3.status_code == 200
    assert len(list1) == len(list2) - 1
    assert set(challenge['id'] for challenge in list1).issubset(set(challenge['id'] for challenge in list2))
    assert post_result in list2
