from . import client
from .data_generator import get_data

def test_post_challenge(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data('example1', 'example_test1', 'Testing', '2', 'example_challenge', 'example_test1')
    with open('tests/ruby/tests-data/example_challenge.rb') as f:
        code_content = f.read()
    with open('tests/ruby/tests-data/example_test1.rb') as f:
        tests_code_content = f.read()

    #act
    r = client.post(url, data=data)
    post_result = r.json['challenge']
    post_result.pop('id')

    #assert
    assert r.status_code == 200
    assert post_result == {
        "code": code_content,
        "tests_code":  tests_code_content,
        "repair_objective": "Testing",
        "complexity": "2",
        "best_score": 0
    }

def test_post_existent_challenge(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data('example7', 'example_test7', 'Testing repeated post', '4', 'example_challenge', 'example_test7')
    r1 = client.post(url, data=data)
    data = get_data('example7', 'example_test7', 'Testing repeated post', '4', 'example_challenge', 'example_test7')

    #act
    r2 = client.post(url, data=data)

    #assert
    assert r1.status_code == 200
    assert r2.status_code == 409
    assert r2.json['challenge'] == 'the source code already exists'

def test_post_code_not_compiles1(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data('example8', 'example_test8', 'Testing compilation error', '4', 'example_not_compile', 'example_test8')

    #act
    r = client.post(url, data=data)

    #assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the source code and/or test suite does not compile'

def test_post_code_not_compiles2(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data('example8', 'example_test8', 'Testing compilation error', '4', 'example_challenge', 'example_not_compile_test8')

    #act
    r = client.post(url, data=data)

    #assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the source code and/or test suite does not compile'

def test_post_bad_dependencies(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data('example8', 'example_test8', 'Testing dependencies error', '4', 'example_challenge', 'example_dependencies_not_okay_test8')

    #act
    r = client.post(url, data=data)

    #assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the test suite dependencies are wrong'

def test_post_no_tests_fail(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data('example9', 'example_test9', 'Testing not errors to repair', '2', 'example_fixed', 'example_test9')

    #act
    r = client.post(url, data=data)

    #assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the challenge has no errors to repair'

def test_post_invalid_data(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data(' ', ' ', ' ', '7', 'example_challenge', 'example_test21')

    #act
    r = client.post(url, data=data)

    #assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the data is incomplete or invalid'

def test_post_invalid_data2(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data('example21', 'example_test21', 'Testing post data', '2', 'example_challenge', 'example_test21')
    data['challenge'] = data['challenge'].replace('challenge', 'challonge')

    #act
    r = client.post(url, data=data)

    #assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the json has no challenge field'

def test_post_without_data(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data(code='example_challenge',tests_code='example_test21')
    data.pop('challenge')

    #act
    r = client.post(url, data=data)

    #assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the code, tests code and json challenge are necessary'

def test_post_without_code(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data('example21', 'example_test21', 'Testing post without code', '4', tests_code='example_test21')

    #act
    r = client.post(url, data=data)

    #assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the code, tests code and json challenge are necessary'

def test_post_without_tests_code(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data('example21', 'example_test21', 'Testing post without tests code', '4', 'example_challenge')

    #act
    r = client.post(url, data=data)

    #assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the code, tests code and json challenge are necessary'

def test_post_invalid_json_format(client):
    #arrange
    url = '/ruby/challenge'
    data = get_data('example24', 'example_test24', 'Testing post invalid format', '2', 'example_challenge', 'example_test24')
    data['challenge'] = data['challenge'].replace('challenge":', 'challenge')

    #act
    r = client.post(url, data=data)

    #assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the json is not in a valid format'