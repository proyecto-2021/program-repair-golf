from . import client
from .data_generator import get_data

def test_post_challenge(client):
    url = '/ruby/challenge'
    data = get_data('example1', 'example_test1', 'Testing', '2', 'example_challenge', 'example_test1')

    with open('tests/ruby/tests-data/example_challenge.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/example_test1.rb') as f:
        content_tests_code = f.read()

    r = client.post(url, data=data)
    json = r.json['challenge']
    del json['id'] #remove the id because it can change if more challenges are stored

    assert r.status_code == 200
    assert json == {  "code": content_code,
                      "tests_code":  content_tests_code,
                      "repair_objective": "Testing",
                      "complexity": "2",
                      "best_score": 0
                      }

def test_post_existent_challenge(client):
    url = '/ruby/challenge'
    data = get_data('example7', 'example_test7', 'Testing repeated post', '4', 'example_challenge', 'example_test7')

    r = client.post(url, data=data)

    url = '/ruby/challenge'
    data = get_data('example7', 'example_test7', 'Testing repeated post', '4', 'example_challenge', 'example_test7')

    r2 = client.post(url, data=data)
    response = r2.json['challenge']

    assert r.status_code == 200
    assert r2.status_code == 409
    assert response == 'source_code already exists'

def test_post_code_not_compiles1(client):
    url = '/ruby/challenge'
    data = get_data('example8', 'example_test8', 'Testing compilation error', '4', 'example_not_compile', 'example_test8')

    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 400
    assert response == 'source_code and/or test_suite doesnt compile'

def test_post_code_not_compiles2(client):
    url = '/ruby/challenge'
    data = get_data('example8', 'example_test8', 'Testing compilation error', '4', 'example_challenge', 'example_not_compile_test8')

    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 400
    assert response == 'source_code and/or test_suite doesnt compile'

def test_post_bad_dependencies(client):
    url = '/ruby/challenge'
    data = get_data('example8', 'example_test8', 'Testing dependencies error', '4', 'example_challenge', 'example_dependencies_not_okay_test8')

    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 400
    assert response == 'test_suite dependencies are wrong'

def test_post_no_tests_fail(client):
    url = '/ruby/challenge'
    data = get_data('example9', 'example_test9', 'Testing not errors to repair', '2', 'example_fixed', 'example_test9')

    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 400
    assert response == 'test_suite doesnt fail'

def test_post_invalid_data(client):
    url = '/ruby/challenge'
    data = get_data(' ', ' ', ' ', '7', 'example_challenge', 'example_test21')
    r = client.post(url, data=data)

    assert r.status_code == 400
    assert r.json['challenge'] == 'data is incomplete or invalid'

def test_post_invalid_data2(client):
    url = '/ruby/challenge'
    data = get_data('example21', 'example_test21', 'Testing post data', '2', 'example_challenge', 'example_test21')
    data['challenge'] = data['challenge'].replace('challenge', 'challonge')
    r = client.post(url, data=data)


    assert r.status_code == 400
    assert r.json['challenge'] == 'the json has no challenge field'

def test_post_without_data(client):
    url = '/ruby/challenge'
    data = get_data(code='example_challenge',tests_code='example_test21')
    data.pop('challenge')
    r = client.post(url, data=data)

    assert r.status_code == 400
    assert r.json['challenge'] == 'code, tests_code and json challenge are necessary'

def test_post_without_code(client):
    url = '/ruby/challenge'
    data = get_data('example21', 'example_test21', 'Testing post without code', '4', tests_code='example_test21')
    r = client.post(url, data=data)

    assert r.status_code == 400
    assert r.json['challenge'] == 'code, tests_code and json challenge are necessary'

def test_post_without_tests_code(client):
    url = '/ruby/challenge'
    data = get_data('example21', 'example_test21', 'Testing post without tests code', '4', 'example_challenge')
    r = client.post(url, data=data)

    assert r.status_code == 400
    assert r.json['challenge'] == 'code, tests_code and json challenge are necessary'

def test_post_invalid_json_format(client):
    url = '/ruby/challenge'
    data = get_data('example24', 'example_test24', 'Testing post invalid format', '2', 'example_challenge', 'example_test24')
    data['challenge'] = data['challenge'].replace('challenge":', 'challenge')
    r = client.post(url, data=data)

    assert r.status_code == 400
    assert r.json['challenge'] == 'the json is not in a valid format'