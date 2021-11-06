from . import client

def get_data(code, tests_code, code_name, tests_name, repair_objective, complexity):
    return {'source_code_file': open(f'tests/ruby/tests-data/{code}.rb', 'rb'),
            'test_suite_file': open(f'tests/ruby/tests-data/{tests_code}.rb', 'rb'),
            'challenge': '{ \
                "challenge": { \
                    ' + f'''"source_code_file_name" : "{code_name}" , \
                    "test_suite_file_name" : "{tests_name}", \
                    "repair_objective" : "{repair_objective}", \
                    "complexity" : "{complexity}" \
                    ''' + ' } \
                }'
            }


def test_post_challenge(client):
    url = '/ruby/challenge'
    data = get_data('example_challenge', 'example_test1', 'example1', 'example_test1', 'Testing', '2')

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


def test_get_one_after_post(client):
    url = '/ruby/challenge'
    data = get_data('example_challenge', 'example_test2', 'example2', 'example_test2', 'Testing', '5')

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

def test_get_all_after_post(client):
    url = '/ruby/challenges'
    r = client.get(url)
    json = r.json['challenges']

    url = '/ruby/challenge'
    data = get_data('example_challenge', 'example_test3', 'example3', 'example_test3', 'Testing', '4')

    r2 = client.post(url, data=data)

    url = '/ruby/challenges'
    r3 = client.get(url)
    json_after_post = r3.json['challenges']

    assert r.status_code == 200
    assert r2.status_code == 200
    assert r3.status_code == 200
    assert len(json) + 1 == len(json_after_post)

def test_post_repair(client):
    url = '/ruby/challenge'
    data = get_data('example_challenge', 'example_test4', 'example4', 'example_test4', 'Testing repair', '3')

    r = client.post(url, data=data)
    id = r.json['challenge']['id']
    url2 = f'/ruby/challenge/{id}/repair'
    data2 = { 'source_code_file': open('tests/ruby/tests-data/example_fixed.rb', 'rb') }
    r2 = client.post(url2, data=data2)

    assert r.status_code == 200
    assert r2.status_code == 200
    assert r2.json['repair']['score'] != 0

def test_put_after_post(client):
    url = '/ruby/challenge'
    data = get_data('example_challenge', 'example_test5', 'example5', 'example_test5', 'Testing pre-PUT', '2')

    r = client.post(url, data=data)
    json = r.json['challenge']
    id = json['id']

    url2 = f'/ruby/challenge/{id}'
    data2 = get_data('example_put5', 'example_test_put5', 'example_put5', 'example_test_put5', 'Testing post-PUT', '3')

    with open('tests/ruby/tests-data/example_put5.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/example_test_put5.rb') as f:
        content_tests_code = f.read()

    r2 = client.put(url2, data=data2)
    dict2 = r2.json['challenge']

    assert r.status_code == 200
    assert r2.status_code == 200
    assert dict2 == {  "code": content_code,
                        "tests_code": content_tests_code,
                        "repair_objective": "Testing post-PUT",
                        "complexity": "3",
                        "best_score": 0
                    }

def test_post_existent_challenge(client):
    url = '/ruby/challenge'
    data = get_data('example_challenge', 'example_test7', 'example7', 'example_test7', 'Testing repeated post', '4')

    r = client.post(url, data=data)

    url = '/ruby/challenge'
    data = get_data('example_challenge', 'example_test7', 'example7', 'example_test7', 'Testing repeated post', '4')

    r2 = client.post(url, data=data)
    response = r2.json['challenge']

    assert r.status_code == 200
    assert r2.status_code == 409
    assert response == 'source_code already exists'

def test_post_code_not_compiles1(client):
    url = '/ruby/challenge'
    data = get_data('example_not_compile8', 'example_test8', 'example8', 'example_test8', 'Testing compilation error', '4')

    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 400
    assert response == 'source_code and/or test_suite not compile'

def test_post_code_not_compiles2(client):
    url = '/ruby/challenge'
    data = get_data('example_challenge', 'example_not_compile_test8', 'example8', 'example_test8', 'Testing compilation error', '4')

    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 400
    assert response == 'source_code and/or test_suite not compile'

def test_post_bad_dependencies(client):
    url = '/ruby/challenge'
    data = get_data('example_challenge', 'example_dependencies_not_okay_test8', 'example8', 'example_test8', 'Testing dependencies error', '4')

    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 400
    assert response == 'test_suite dependencies are wrong'

def test_post_no_tests_fail(client):
    url = '/ruby/challenge'
    data = get_data('example_fixed', 'example_test9', 'example9', 'example_test9', 'Testing not errors to repair', '2')

    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 400
    assert response == 'test_suite does not fail'

def test_post_repair_invalid_challenge(client):
    url = '/ruby/challenge/1000/repair' #its probably that we dont post 1000 challenges for test
    data = { 'source_code_file': open('tests/ruby/tests-data/example_fixed.rb','rb') }
    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 404
    assert response == 'NOT FOUND'

def test_post_repair_candidate_compiles_error(client):
    url = '/ruby/challenge'
    data = get_data('example_challenge', 'example_test10', 'example10', 'example_test10', 'Testing repair candidate does not compile', '3')

    r = client.post(url, data=data)
    id = r.json['challenge']['id']

    url2 = f'/ruby/challenge/{id}/repair'
    data2 = { 'source_code_file': open('tests/ruby/tests-data/example_fixed_syntax_error.rb', 'rb') }
    r2 = client.post(url2, data=data2)

    assert r.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == {'repair_code': 'is erroneous'}

def test_post_repair_candidate_tests_fail(client):
    url = '/ruby/challenge'
    data = get_data('example_challenge', 'example_test11', 'example11', 'example_test11', 'Testing repair candidate fail tests', '2')

    r = client.post(url, data=data)
    id = r.json['challenge']['id']

    url2 = f'/ruby/challenge/{id}/repair'
    data2 = { 'source_code_file': open('tests/ruby/tests-data/example_challenge.rb', 'rb') }
    r2 = client.post(url2, data=data2)

    assert r.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] == {'tests_code': 'fails'}