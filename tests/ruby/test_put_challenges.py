from . import client, auth
from .data_generator import get_data

def test_put_after_post(client, auth):
    #arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example5', 'example_test5', 'Testing pre-PUT', '2', 'example_challenge', 'example_test5')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    id = r1.json['challenge']['id']
    url2 = f'/ruby/challenge/{id}'
    data2 = get_data('example_put5', 'example_test_put5', 'Testing post-PUT', '3', 'example_put5', 'example_test_put5')
    with open('tests/ruby/tests-data/example_put5.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/example_test_put5.rb') as f:
        content_tests_code = f.read()

    #act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] == {
        "code": content_code,
        "tests_code": content_tests_code,
        "repair_objective": "Testing post-PUT",
        "complexity": "3",
        "best_score": 0
    }

def test_put_only_change_files_names(client, auth):
    #arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example12', 'example_test12', 'Testing put change files names', '1', 'example_challenge', 'example_test12')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    id = r1.json['challenge']['id']
    orig_json = r1.json['challenge']
    orig_json.pop('id')
    url2 = f'/ruby/challenge/{id}'
    data2 = get_data('example', 'example_test12', 'Testing put', '3')

    #act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})
    r3 = client.get(url2, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r1.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == 'the test suite dependencies are wrong'
    assert r3.json['challenge'] == orig_json

def test_put_code_not_compiles1(client, auth):
    #arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example13', 'example_test13', 'Testing', '4','example_challenge', 'example_test13')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    id = r1.json['challenge']['id']
    orig_json = r1.json['challenge']
    orig_json.pop('id')
    url2 = f'/ruby/challenge/{id}'
    data2 = get_data('example13', 'example_test13', 'Testing put code does not compiles', '3', 'example_not_compile', 'example_test13')

    #act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})
    r3 = client.get(url2, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r1.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == 'the source code does not compile'
    assert r3.json['challenge'] == orig_json

def test_put_code_not_compiles2(client, auth):
    #arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example14', 'example_test14', 'Testing', '5', 'example_challenge', 'example_test14')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    id = r1.json['challenge']['id']
    orig_json = r1.json['challenge']
    orig_json.pop('id')
    url2 = f'/ruby/challenge/{id}'
    data2 = get_data('example14', 'example_test14', 'Testing put code does not compiles', '2', 'example_challenge', 'example_test_no_compiles14')

    #act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})
    r3 = client.get(url2, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r1.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == 'the test suite does not compile'
    assert r3.json['challenge'] == orig_json

def test_put_with_update_info_existent(client, auth):
    #arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example15', 'example_test15', 'Testing', '3', 'example_challenge', 'example_test15')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    data2 = get_data('example16', 'example_test16', 'Testing', '1','example_challenge', 'example_test16')
    r2 = client.post(url1, data=data2, headers={'Authorization': f'JWT {auth}'})
    id = r2.json['challenge']['id']
    orig_json = r2.json['challenge']
    orig_json.pop('id')
    url2 = f'/ruby/challenge/{id}'
    data3 = get_data('example15', 'example_test15', 'Testing put ', '2', 'example_challenge', 'example_test15')

    #assert
    r3 = client.put(url2, data=data3, headers={'Authorization': f'JWT {auth}'})
    r4 = client.get(url2, headers={'Authorization': f'JWT {auth}'})

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r3.status_code == 409
    assert r3.json['challenge'] == 'the code file name already exists'
    assert r4.json['challenge'] == orig_json

def test_put_new_tests_and_rename_code(client, auth):
    #arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example17', 'example_test17', 'Testing', '4', 'example_challenge', 'example_test17')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    id = r1.json['challenge']['id']
    url2 = f'/ruby/challenge/{id}'
    data2 = get_data('example18', 'example_test18', 'Testing put new tests and rename code', '4', tests_code='example_test18')
    with open('tests/ruby/tests-data/example_challenge.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/example_test18.rb') as f:
        content_tests_code = f.read()

    #act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] ==  {
        "code": content_code,
        "tests_code": content_tests_code,
        "repair_objective": "Testing put new tests and rename code",
        "complexity": "4",
        "best_score": 0
    }

def test_put_only_new_data(client, auth):
    #arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example19', 'example_test19', 'Testing', '4', 'example_challenge', 'example_test19')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    id = r1.json['challenge']['id']
    url2 = f'/ruby/challenge/{id}'
    data2 = get_data(None, None, 'Testing put only new data', '2')
    with open('tests/ruby/tests-data/example_challenge.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/example_test19.rb') as f:
        content_tests_code = f.read()

    #act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] ==  {
        "code": content_code,
        "tests_code": content_tests_code,
        "repair_objective": "Testing put only new data",
        "complexity": "2",
        "best_score": 0
    }

def test_put_only_codes(client, auth):
    #arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example20', 'example_test20', 'Testing put only new codes', '4', 'example_challenge', 'example_test20')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    id = r1.json['challenge']['id']
    url2 = f'/ruby/challenge/{id}'
    data2 = get_data(code='example_challenge_new', tests_code='example_test20new')
    data2.pop('challenge')
    with open('tests/ruby/tests-data/example_challenge_new.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/example_test20new.rb') as f:
        content_tests_code = f.read()

    #act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] ==  {
        "code": content_code,
        "tests_code": content_tests_code,
        "repair_objective": "Testing put only new codes",
        "complexity": "4",
        "best_score": 0
    }

def test_put_invalid_challenge(client, auth):
    #arrange
    url = '/ruby/challenge/1000'
    data = get_data(None, None, 'Testing put only new data', '2')

    #act
    r = client.put(url, data=data, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r.status_code == 404
    assert r.json['challenge'] == 'the id does not exist'

def test_put_invalid_data(client, auth):
    #arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example23', 'example_test23', 'Testing put invalid data', '1', 'example_challenge', 'example_test23')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    id = r1.json['challenge']['id']
    orig_json = r1.json['challenge']
    orig_json.pop('id')
    data2 = get_data(' ', ' ', ' ', '0')
    url2 = f'/ruby/challenge/{id}'

    #act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})
    r3 = client.get(url2, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r1.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == 'the data is incomplete or invalid'
    assert r3.json['challenge'] == orig_json

def test_put_invalid_data2(client, auth):
    url1 = '/ruby/challenge'
    data1 = get_data('example24', 'example_test24', 'Testing put invalid data', '1', 'example_challenge', 'example_test24')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    id = r1.json['challenge']['id']
    orig_json = r1.json['challenge']
    orig_json.pop('id')
    data2 = get_data('example24', 'example_test25', 'Testing put invalid data', '3')
    data2['challenge'] = data2['challenge'].replace('challenge', 'challonge')
    url2 = f'/ruby/challenge/{id}'

    #act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})
    r3 = client.get(url2, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r1.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == 'the json has no challenge field'
    assert r3.json['challenge'] == orig_json

def test_put_invalid_json_format(client, auth):
    #arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example25', 'example_test25', 'Testing put invalid format', '1', 'example_challenge', 'example_test25')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    id = r1.json['challenge']['id']
    orig_json = r1.json['challenge']
    orig_json.pop('id')
    data2 = get_data('example25', 'example_test26', 'Testing put invalid format', '3')
    data2['challenge'] = data2['challenge'].replace('challenge":', 'challenge')
    url2 = f'/ruby/challenge/{id}'

    #act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})
    r3 = client.get(url2, headers={'Authorization': f'JWT {auth}'})

    #assert
    assert r1.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == 'the json is not in a valid format'
    assert r3.json['challenge'] == orig_json