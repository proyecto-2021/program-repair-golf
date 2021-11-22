from . import client, auth, generic_post
from .data_generator import get_data


def test_put_after_post(client, auth):
    # arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example2', 'example_test2', 'Testing pre-PUT', '2', 'example_median', 'example_test2')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    challenge_id = r1.json['challenge']['id']
    url2 = f'/ruby/challenge/{challenge_id}'
    data2 = get_data('example_factorial', 'example_factorial_test', 'Testing post-PUT', '3',
                     'example_factorial', 'example_factorial_test')
    with open('tests/ruby/tests-data/example_factorial.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/example_factorial_test.rb') as f:
        content_tests_code = f.read()

    # act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] == {
        "code": content_code,
        "tests_code": content_tests_code,
        "repair_objective": "Testing post-PUT",
        "complexity": "3",
        "best_score": 0
    }


def test_put_only_change_files_names(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    orig_json.pop('id')
    url = f'/ruby/challenge/{challenge_id}'
    data = get_data('example2', 'example_test2', 'Testing put', '3')

    # act
    r1 = client.put(url, data=data, headers={'Authorization': f'JWT {auth}'})
    r2 = client.get(url, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 400
    assert r1.json['challenge'] == 'the test suite dependencies are wrong'
    assert r2.json['challenge'] == orig_json


def test_put_code_not_compiles1(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    orig_json.pop('id')
    url = f'/ruby/challenge/{challenge_id}'
    data = get_data('example', 'example_test', 'Testing put code does not compiles', '3',
                    'example_not_compiles', 'example_test1')

    # act
    r1 = client.put(url, data=data, headers={'Authorization': f'JWT {auth}'})
    r2 = client.get(url, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 400
    assert r1.json['challenge'] == 'the source code does not compile'
    assert r2.json['challenge'] == orig_json


def test_put_code_not_compiles2(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    orig_json.pop('id')
    url = f'/ruby/challenge/{challenge_id}'
    data = get_data('example', 'example_test', 'Testing put code does not compiles', '2',
                    'example_median', 'example_test_not_compiles')

    # act
    r1 = client.put(url, data=data, headers={'Authorization': f'JWT {auth}'})
    r2 = client.get(url, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 400
    assert r1.json['challenge'] == 'the test suite does not compile'
    assert r2.json['challenge'] == orig_json


def test_put_with_update_info_existent(client, auth, generic_post):
    # arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example2', 'example_test2', 'Testing', '1', 'example_median', 'example_test2')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    data2 = get_data('example3', 'example_test3', 'Testing', '1', 'example_max', 'example_test3')
    r2 = client.post(url1, data=data2, headers={'Authorization': f'JWT {auth}'})
    challenge_id = r2.json['challenge']['id']
    orig_json = r2.json['challenge']
    orig_json.pop('id')
    url2 = f'/ruby/challenge/{challenge_id}'
    data3 = get_data('example2', 'example_test2', 'Testing put ', '2',
                     'example_median', 'example_test2')

    # assert
    r3 = client.put(url2, data=data3, headers={'Authorization': f'JWT {auth}'})
    r4 = client.get(url2, headers={'Authorization': f'JWT {auth}'})

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r3.status_code == 409
    assert r3.json['challenge'] == 'the code file name already exists'
    assert r4.json['challenge'] == orig_json


def test_put_new_tests_and_rename_code(client, auth):
    # arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example4', 'example_test4', 'Testing', '4', 'example_median', 'example_test4')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    challenge_id = r1.json['challenge']['id']
    url2 = f'/ruby/challenge/{challenge_id}'
    data2 = get_data('new_example4', 'example_test4', 'Testing put new tests and rename code', '4',
                     tests_code='new_example_test4')
    with open('tests/ruby/tests-data/example_median.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/new_example_test4.rb') as f:
        content_tests_code = f.read()

    # act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] == {
        "code": content_code,
        "tests_code": content_tests_code,
        "repair_objective": "Testing put new tests and rename code",
        "complexity": "4",
        "best_score": 0
    }


def test_put_only_new_data(client, auth):
    # arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example_max', 'example_max_test', 'Testing', '4', 'example_max', 'example_max_test')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    challenge_id = r1.json['challenge']['id']
    url2 = f'/ruby/challenge/{challenge_id}'
    data2 = get_data(None, None, 'Testing put only new data', '2')
    with open('tests/ruby/tests-data/example_max.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/example_max_test.rb') as f:
        content_tests_code = f.read()

    # act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] == {
        "code": content_code,
        "tests_code": content_tests_code,
        "repair_objective": "Testing put only new data",
        "complexity": "2",
        "best_score": 0
    }


def test_put_only_codes(client, auth):
    # arrange
    url1 = '/ruby/challenge'
    data1 = get_data('example5', 'example_test5', 'Testing put only new codes', '4',
                     'example_fibonacci', 'example_test5')
    r1 = client.post(url1, data=data1, headers={'Authorization': f'JWT {auth}'})
    challenge_id = r1.json['challenge']['id']
    url2 = f'/ruby/challenge/{challenge_id}'
    data2 = get_data(code='new_example', tests_code='new_example_test5')
    data2.pop('challenge')
    with open('tests/ruby/tests-data/new_example.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/new_example_test5.rb') as f:
        content_tests_code = f.read()

    # act
    r2 = client.put(url2, data=data2, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] == {
        "code": content_code,
        "tests_code": content_tests_code,
        "repair_objective": "Testing put only new codes",
        "complexity": "4",
        "best_score": 0
    }


def test_put_invalid_challenge(client, auth):
    # arrange
    url = '/ruby/challenge/1000'
    data = get_data(None, None, 'Testing put only new data', '2')

    # act
    r = client.put(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 404
    assert r.json['challenge'] == 'the id does not exist'


def test_put_invalid_data1(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    orig_json.pop('id')
    data = get_data(' ', ' ', ' ', '0')
    url = f'/ruby/challenge/{challenge_id}'

    # act
    r1 = client.put(url, data=data, headers={'Authorization': f'JWT {auth}'})
    r2 = client.get(url, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 400
    assert r1.json['challenge'] == 'the data is incomplete or invalid'
    assert r2.json['challenge'] == orig_json


def test_put_invalid_data2(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    orig_json.pop('id')
    data = get_data('example', 'example_test', 'Testing put invalid data', '3')
    data['challenge'] = data['challenge'].replace('challenge', 'challenges')
    url = f'/ruby/challenge/{challenge_id}'

    # act
    r1 = client.put(url, data=data, headers={'Authorization': f'JWT {auth}'})
    r2 = client.get(url, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 400
    assert r1.json['challenge'] == 'the json has no challenge field'
    assert r2.json['challenge'] == orig_json


def test_put_invalid_json_format(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    orig_json.pop('id')
    data = get_data('example', 'example_test', 'Testing put invalid format', '3')
    data['challenge'] = data['challenge'].replace('challenge":', 'challenge')
    url = f'/ruby/challenge/{challenge_id}'

    # act
    r1 = client.put(url, data=data, headers={'Authorization': f'JWT {auth}'})
    r2 = client.get(url, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 400
    assert r1.json['challenge'] == 'the json is not in a valid format'
    assert r2.json['challenge'] == orig_json


def test_put_invalid_attributes1(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    orig_json.pop('id')
    data = get_data('example', 'example_test', 'Testing put invalid format', '3')
    data['challenge'] = data['challenge'].replace('complexity', 'bad_attribute')
    url = f'/ruby/challenge/{challenge_id}'

    # act
    r1 = client.put(url, data=data, headers={'Authorization': f'JWT {auth}'})
    r2 = client.get(url, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 400
    assert r1.json['challenge'] == 'the json has invalid attributes'
    assert r2.json['challenge'] == orig_json


def test_put_invalid_attributes2(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    orig_json.pop('id')
    data = get_data('example', 'example_test', 'Testing put invalid format', '3')
    # The best score can be updated in put, only in post repair
    data['challenge'] = data['challenge'].replace('"complexity": "3"', '"best_score": 0')
    url = f'/ruby/challenge/{challenge_id}'

    # act
    r1 = client.put(url, data=data, headers={'Authorization': f'JWT {auth}'})
    r2 = client.get(url, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 400
    assert r1.json['challenge'] == 'the json has invalid attributes'
    assert r2.json['challenge'] == orig_json


def test_put_without_authentication(client):
    # arrange
    url = '/ruby/challenge/1000'

    # act
    r = client.put(url)

    # assert
    assert r.status_code == 401
    assert r.json['error'] == 'Authorization Required'
