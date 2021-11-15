from . import client
from .data_generator import get_data

def test_post_repair(client):
    url = '/ruby/challenge'
    data = get_data('example4', 'example_test4', 'Testing repair', '3', 'example_challenge', 'example_test4')

    r = client.post(url, data=data)
    id = r.json['challenge']['id']
    url2 = f'/ruby/challenge/{id}/repair'
    data2 = { 'source_code_file': open('tests/ruby/tests-data/example_fixed.rb', 'rb') }
    r2 = client.post(url2, data=data2)

    assert r.status_code == 200
    assert r2.status_code == 200
    assert r2.json['repair']['score'] != 0

def test_post_repair_invalid_challenge(client):
    url = '/ruby/challenge/1000/repair' #its probably that we dont post 1000 challenges for test
    data = { 'source_code_file': open('tests/ruby/tests-data/example_fixed.rb','rb') }
    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 404
    assert response == 'id doesnt exist'

def test_post_repair_candidate_compiles_error(client):
    url = '/ruby/challenge'
    data = get_data('example10', 'example_test10', 'Testing repair candidate does not compile', '3', 'example_challenge', 'example_test10')

    r = client.post(url, data=data)
    id = r.json['challenge']['id']

    url2 = f'/ruby/challenge/{id}/repair'
    data2 = { 'source_code_file': open('tests/ruby/tests-data/example_fixed_no_compiles.rb', 'rb') }
    r2 = client.post(url2, data=data2)

    assert r.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == {'repair_code': 'is erroneous'}

def test_post_repair_candidate_tests_fail(client):
    url = '/ruby/challenge'
    data = get_data('example11', 'example_test11', 'Testing repair candidate fail tests', '2', 'example_challenge', 'example_test11')

    r = client.post(url, data=data)
    id = r.json['challenge']['id']

    url2 = f'/ruby/challenge/{id}/repair'
    data2 = { 'source_code_file': open('tests/ruby/tests-data/example_challenge.rb', 'rb') }
    r2 = client.post(url2, data=data2)

    assert r.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] == {'tests_code': 'fails'}

def test_post_repair_without_repair_candidate(client):
    url = '/ruby/challenge'
    data = get_data('example22', 'example_test22', 'Testing post repair without code', '4', 'example_challenge', 'example_test22')
    r = client.post(url, data=data)
    id = r.json['challenge']['id']


    url2 = f'/ruby/challenge/{id}/repair'
    r2 = client.post(url2)

    assert r.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == 'repair_code is necessary'