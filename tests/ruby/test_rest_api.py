from . import client

def get_data(code_name=None, tests_name=None, repair_objective=None, complexity=None, code=None, tests_code=None):
    data = dict()
    if code is not None:
        data.update({'source_code_file': open(f'tests/ruby/tests-data/{code}.rb', 'rb')})
    if tests_code is not None:
        data.update({'test_suite_file': open(f'tests/ruby/tests-data/{tests_code}.rb', 'rb')})

    data.update(get_json(code_name, tests_name, repair_objective, complexity))
    return data

def get_json(code_name=None, tests_name=None, repair_objective=None, complexity=None):
    dictionary = { 'source_code_file_name': code_name, 'test_suite_file_name': tests_name, 'repair_objective': repair_objective, 'complexity': complexity }
    data = '{ "challenge": { '
    first = True
    for key in dictionary:
        if dictionary[key] is not None:
            if first:
                data = data + f'"{key}" : "{dictionary[key]}"'
                first = False
            else:
                data = data + f', "{key}" : "{dictionary[key]}"'

    data = data + ' } }'
    return {'challenge': data}

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


def test_get_one_after_post(client):
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

def test_put_after_post(client):
    url = '/ruby/challenge'
    data = get_data('example5', 'example_test5', 'Testing pre-PUT', '2', 'example_challenge', 'example_test5')

    r = client.post(url, data=data)
    json = r.json['challenge']
    id = json['id']

    url2 = f'/ruby/challenge/{id}'
    data2 = get_data('example_put5', 'example_test_put5', 'Testing post-PUT', '3', 'example_put5', 'example_test_put5')

    r2 = client.put(url2, data=data2)
    dict2 = r2.json['challenge']

    with open('tests/ruby/tests-data/example_put5.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/example_test_put5.rb') as f:
        content_tests_code = f.read()

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

def test_put_only_change_files_names(client):
    url = '/ruby/challenge'
    data = get_data('example12', 'example_test12', 'Testing put change files names', '1', 'example_challenge', 'example_test12')

    r = client.post(url, data=data)
    id = r.json['challenge']['id']

    url2 = f'/ruby/challenge/{id}'
    data2 = get_json('example', 'example_test12', 'Testing put', '3')

    r2 = client.put(url2, data=data2)

    assert r.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == 'test_suite dependencies are wrong'

def test_put_code_not_compiles1(client):
    url = '/ruby/challenge'
    data = get_data('example13', 'example_test13', 'Testing', '4','example_challenge', 'example_test13')

    r = client.post(url, data=data)
    id = r.json['challenge']['id']

    url2 = f'/ruby/challenge/{id}'
    data2 = get_data('example13', 'example_test13', 'Testing put code does not compiles', '3', 'example_not_compile', 'example_test13')

    r2 = client.put(url2, data=data2)

    assert r.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == 'code doesnt compile'

def test_put_code_not_compiles2(client):
    url = '/ruby/challenge'
    data = get_data('example14', 'example_test14', 'Testing', '5', 'example_challenge', 'example_test14')

    r = client.post(url, data=data)
    id = r.json['challenge']['id']

    url2 = f'/ruby/challenge/{id}'
    data2 = get_data('example14', 'example_test14', 'Testing put code does not compiles', '2', 'example_challenge', 'example_test_no_compiles14')

    r2 = client.put(url2, data=data2)

    assert r.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == 'test_suite doesnt compile'

def test_put_with_update_info_existent(client):
    url = '/ruby/challenge'
    data = get_data('example15', 'example_test15', 'Testing', '3', 'example_challenge', 'example_test15')
    r1 = client.post(url, data=data)

    url = '/ruby/challenge'
    data = get_data('example16', 'example_test16', 'Testing', '1','example_challenge', 'example_test16')

    r2 = client.post(url, data=data)
    id = r2.json['challenge']['id']

    url2 = f'/ruby/challenge/{id}'
    data2 = get_data('example15', 'example_test15', 'Testing put ', '2', 'example_challenge', 'example_test15')

    r3 = client.put(url2, data=data2)

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r3.status_code == 409
    assert r3.json['challenge'] == 'code_file_name already exists'

def test_put_new_tests_and_rename_code(client):
    url = '/ruby/challenge'
    data = get_data('example17', 'example_test17', 'Testing', '4', 'example_challenge', 'example_test17')
    r1 = client.post(url, data=data)
    id = r1.json['challenge']['id']

    url2 = f'/ruby/challenge/{id}'
    data2 = get_data('example18', 'example_test18', 'Testing put new tests and rename code', '4', tests_code='example_test18')

    r2 = client.put(url2, data=data2)

    with open('tests/ruby/tests-data/example_challenge.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/example_test18.rb') as f:
        content_tests_code = f.read()

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] ==  {
        "code": content_code,
        "tests_code": content_tests_code,
        "repair_objective": "Testing put new tests and rename code",
        "complexity": "4",
        "best_score": 0
    }

def test_put_only_new_data(client):
    url = '/ruby/challenge'
    data = get_data('example19', 'example_test19', 'Testing', '4', 'example_challenge', 'example_test19')
    r1 = client.post(url, data=data)
    id = r1.json['challenge']['id']

    url2 = f'/ruby/challenge/{id}'
    data2 = get_data(None, None, 'Testing put only new data', '2')

    r2 = client.put(url2, data=data2)

    with open('tests/ruby/tests-data/example_challenge.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/example_test19.rb') as f:
        content_tests_code = f.read()

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] ==  {
        "code": content_code,
        "tests_code": content_tests_code,
        "repair_objective": "Testing put only new data",
        "complexity": "2",
        "best_score": 0
    }

def test_put_only_codes(client):
    url = '/ruby/challenge'
    data = get_data('example20', 'example_test20', 'Testing put only new codes', '4', 'example_challenge', 'example_test20')
    r1 = client.post(url, data=data)
    id = r1.json['challenge']['id']

    url2 = f'/ruby/challenge/{id}'
    data2 = get_data(code='example_challenge_new', tests_code='example_test20new')

    r2 = client.put(url2, data=data2)

    with open('tests/ruby/tests-data/example_challenge_new.rb') as f:
        content_code = f.read()
    with open('tests/ruby/tests-data/example_test20new.rb') as f:
        content_tests_code = f.read()

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r2.json['challenge'] ==  {
        "code": content_code,
        "tests_code": content_tests_code,
        "repair_objective": "Testing put only new codes",
        "complexity": "4",
        "best_score": 0
    }

def test_get_invalid_challenge(client):
    url = '/ruby/challenge/1000'

    r = client.get(url)

    assert r.status_code == 404
    assert r.json['challenge'] == 'id doesnt exist'

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

def test_put_invalid_challenge(client):
    url = '/ruby/challenge/1000'
    data = get_data(None, None, 'Testing put only new data', '2')
    r = client.put(url, data=data)

    assert r.status_code == 404
    assert r.json['challenge'] == 'id doesnt exist'

def test_post_invalid_data(client):
    url = '/ruby/challenge'
    data = get_data(' ', ' ', ' ', '7', 'example_challenge', 'example_test21')
    r = client.post(url, data=data)

    assert r.status_code == 400
    assert r.json['challenge'] == 'data is incomplete or invalid'

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

def test_put_invalid_data(client):
    url = '/ruby/challenge'
    data = get_data('example23', 'example_test23', 'Testing put invalid data', '1', 'example_challenge', 'example_test23')
    r = client.post(url, data=data)
    id = r.json['challenge']['id']

    data2 = get_data(' ', ' ', ' ', '0')
    url2 = f'/ruby/challenge/{id}'
    r2 = client.put(url2, data=data2)

    assert r.status_code == 200
    assert r2.status_code == 400
    assert r2.json['challenge'] == 'data is incomplete or invalid'