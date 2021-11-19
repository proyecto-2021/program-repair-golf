from . import client, auth, generic_post
from .data_generator import get_data

def test_post_repair(client, auth, generic_post):
    #arrange
    orig_json = generic_post['challenge'].copy()
    id = orig_json['id']
    url = f'/ruby/challenge/{id}/repair'
    data = { 'source_code_file': open('tests/ruby/tests-data/example_fixed.rb', 'rb') }

    #act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r.status_code == 200
    assert r.json['repair']['score'] != 0
    assert r.json['repair']['player']['username'] == 'ruby'
    assert r.json['repair']['attempts'] == '1'

def test_post_repair_invalid_challenge(client, auth):
    #arrange
    url = '/ruby/challenge/1000/repair' #its probably that we dont post 1000 challenges for test
    data = { 'source_code_file': open('tests/ruby/tests-data/example_fixed.rb','rb') }

    #act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r.status_code == 404
    assert r.json['challenge'] == 'the id does not exist'

def test_post_repair_candidate_compiles_error(client, auth, generic_post):
    #arrange
    orig_json = generic_post['challenge'].copy()
    id = orig_json['id']
    url = f'/ruby/challenge/{id}/repair'
    data = {'source_code_file': open('tests/ruby/tests-data/example_not_compiles.rb', 'rb')}

    #act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the repair candidate has syntax errors'

def test_post_repair_candidate_tests_fail(client, auth, generic_post):
    #arrange
    orig_json = generic_post['challenge'].copy()
    id = orig_json['id']
    url = f'/ruby/challenge/{id}/repair'
    data = { 'source_code_file': open('tests/ruby/tests-data/example.rb', 'rb') }

    #act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r.status_code == 200
    assert r.json['challenge'] == 'the repair candidate does not solve the problem'

def test_post_repair_without_repair_candidate(client, auth, generic_post):
    #arrange
    orig_json = generic_post['challenge'].copy()
    id = orig_json['id']
    url = f'/ruby/challenge/{id}/repair'

    #act
    r = client.post(url, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'a repair candidate is necessary'