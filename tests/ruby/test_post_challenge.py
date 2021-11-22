from . import client, auth
from .data_generator import get_data


def test_post_challenge(client, auth):
    # arrange
    url = '/ruby/challenge'
    data = get_data('example_addition', 'example_addition_test', 'Testing', '2',
                    'example_addition', 'example_addition_test')
    with open('tests/ruby/tests-data/example_addition.rb') as f:
        code_content = f.read()
    with open('tests/ruby/tests-data/example_addition_test.rb') as f:
        tests_code_content = f.read()

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})
    post_result = r.json['challenge']
    post_result.pop('id')

    # assert
    assert r.status_code == 200
    assert post_result == {
        "code": code_content,
        "tests_code":  tests_code_content,
        "repair_objective": "Testing",
        "complexity": "2",
        "best_score": 0
    }


def test_post_existent_challenge(client, auth):
    # arrange
    url = '/ruby/challenge'
    data = get_data('example1', 'example_test1', 'Testing repeated post', '4', 'example_median', 'example_test1')
    r1 = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})
    data = get_data('example1', 'example_test1', 'Testing repeated post', '4', 'example_median', 'example_test1')

    # act
    r2 = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r1.status_code == 200
    assert r2.status_code == 409
    assert r2.json['challenge'] == 'the source code already exists'


def test_post_code_not_compiles1(client, auth):
    # arrange
    url = '/ruby/challenge'
    data = get_data('example2', 'example_test2', 'Testing compilation error', '4',
                    'example_not_compiles', 'example_test1')

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the source code and/or test suite does not compile'


def test_post_code_not_compiles2(client, auth):
    # arrange
    url = '/ruby/challenge'
    data = get_data('example2', 'example_test2', 'Testing compilation error', '4',
                    'example_median', 'example_test_not_compiles')

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the source code and/or test suite does not compile'


def test_post_bad_dependencies1(client, auth):
    # arrange
    url = '/ruby/challenge'
    data = get_data('example2', 'example_test2', 'Testing dependencies error', '4',
                    'example_median', 'example_test_bad_dependencies1')

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the test suite dependencies are wrong'


def test_post_bad_dependencies2(client, auth):
    # arrange
    url = '/ruby/challenge'
    # 0 dependencies
    data = get_data('example2', 'example_test2', 'Testing dependencies error', '4',
                    'example_median', 'example_test_bad_dependencies2')

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the test suite dependencies are wrong'


def test_post_bad_dependencies3(client, auth):
    # arrange
    url = '/ruby/challenge'
    # More than 1 require_relative
    data = get_data('example2', 'example_test2', 'Testing dependencies error', '4',
                    'example_median', 'example_test_bad_dependencies3')

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the test suite dependencies are wrong'


def test_post_no_tests_fail(client, auth):
    # arrange
    url = '/ruby/challenge'
    data = get_data('example2', 'example_test2', 'Testing not errors to repair', '2',
                    'example_fixed1', 'example_test_fixed')

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the challenge has no errors to repair'


def test_post_invalid_data1(client, auth):
    # arrange
    url = '/ruby/challenge'
    data = get_data(' ', ' ', ' ', '7', 'example_median', 'example_median_test')

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the data is incomplete or invalid'


def test_post_invalid_data2(client, auth):
    # arrange
    url = '/ruby/challenge'
    data = get_data('example', 'example_test', 'Testing post data', '2', 'example_median', 'example_median_test')
    data['challenge'] = data['challenge'].replace('challenge', 'challenges')

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the json has no challenge field'


def test_post_without_data(client, auth):
    # arrange
    url = '/ruby/challenge'
    data = get_data(code='example_median', tests_code='example_median_test')
    data.pop('challenge')

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the code, tests code and json challenge are necessary'


def test_post_without_code(client, auth):
    # arrange
    url = '/ruby/challenge'
    data = get_data('example', 'example_test', 'Testing post without code', '4', tests_code='example_median_test')

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the code, tests code and json challenge are necessary'


def test_post_without_tests_code(client, auth):
    # arrange
    url = '/ruby/challenge'
    data = get_data('example', 'example_test', 'Testing post without tests code', '4', 'example_median')

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the code, tests code and json challenge are necessary'


def test_post_invalid_json_format(client, auth):
    # arrange
    url = '/ruby/challenge'
    data = get_data('example', 'example_test', 'Testing post invalid format', '2',
                    'example_median', 'example_median_test')
    data['challenge'] = data['challenge'].replace('challenge":', 'challenge')

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the json is not in a valid format'


def test_post_without_authentication(client):
    # arrange
    url = '/ruby/challenge'

    # act
    r = client.post(url)

    # assert
    assert r.status_code == 401
    assert r.json['error'] == 'Authorization Required'
