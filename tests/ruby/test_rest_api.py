from . import client

def test_post_challenge(client):
    url = '/ruby/challenge'
    data = {
        'source_code_file': open('tests/ruby/tests-data/example1.rb','rb'),
        'test_suite_file': open('tests/ruby/tests-data/example_test1.rb','rb'),
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "example1", \
                "test_suite_file_name" : "example_test1", \
                "repair_objective" : "Testing", \
                "complexity" : "2" \
            } \
        }'
    }

    with open('tests/ruby/tests-data/example1.rb') as f:
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
    data = {
        'source_code_file': open('tests/ruby/tests-data/example2.rb', 'rb'),
        'test_suite_file': open('tests/ruby/tests-data/example_test2.rb', 'rb'),
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "example2", \
                "test_suite_file_name" : "example_test2", \
                "repair_objective" : "Testing", \
                "complexity" : "5" \
            } \
        }'
    }

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
    data = {
        'source_code_file': open('tests/ruby/tests-data/example3.rb', 'rb'),
        'test_suite_file': open('tests/ruby/tests-data/example_test3.rb', 'rb'),
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "example3", \
                "test_suite_file_name" : "example_test3", \
                "repair_objective" : "Testing", \
                "complexity" : "4" \
            } \
        }'
    }

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
    data = {
        'source_code_file': open('tests/ruby/tests-data/example4.rb', 'rb'),
        'test_suite_file': open('tests/ruby/tests-data/example_test4.rb', 'rb'),
        'challenge': '{ \
                "challenge": { \
                    "source_code_file_name" : "example4", \
                    "test_suite_file_name" : "example_test4", \
                    "repair_objective" : "Testing repair", \
                    "complexity" : "3" \
                } \
            }'
    }

    r = client.post(url, data=data)
    id = r.json['challenge']['id']
    url2 = f'/ruby/challenge/{id}/repair'
    data2 = { 'source_code_file': open('tests/ruby/tests-data/example_fixed4.rb', 'rb') }
    r2 = client.post(url2, data=data2)

    assert r.status_code == 200
    assert r2.status_code == 200
    assert r2.json['repair']['score'] != 0

def test_put_after_post(client):
    url = '/ruby/challenge'
    data = {
        'source_code_file': open('tests/ruby/tests-data/example5.rb', 'rb'),
        'test_suite_file': open('tests/ruby/tests-data/example_test5.rb', 'rb'),
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "example5", \
                "test_suite_file_name" : "example_test5", \
                "repair_objective" : "Testing pre-PUT", \
                "complexity" : "2" \
            } \
        }'
    }

    r = client.post(url, data=data)
    json = r.json['challenge']
    id = json['id']

    url2 = f'/ruby/challenge/{id}'
    data2 = {
        'source_code_file': open('tests/ruby/tests-data/example_put5.rb','rb'),
        'test_suite_file' : open('tests/ruby/tests-data/example_test_put5.rb','rb'),
        'challenge' : '{ \
            "challenge": { \
                "source_code_file_name": "example_put5", \
                "test_suite_file_name": "example_test_put5", \
                "repair_objective": "Testing post-PUT", \
                "complexity": "3" \
            } \
        }'
    }

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
    data = {
        'source_code_file': open('tests/ruby/tests-data/example7.rb', 'rb'),
        'test_suite_file': open('tests/ruby/tests-data/example_test7.rb', 'rb'),
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "example7", \
                "test_suite_file_name" : "example_test7", \
                "repair_objective" : "Testing repeated post", \
                "complexity" : "4" \
            } \
        }'
    }

    r = client.post(url, data=data)

    url = '/ruby/challenge'
    data = {
        'source_code_file': open('tests/ruby/tests-data/example7.rb', 'rb'),
        'test_suite_file': open('tests/ruby/tests-data/example_test7.rb', 'rb'),
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "example7", \
                "test_suite_file_name" : "example_test7", \
                "repair_objective" : "Testing repeated post", \
                "complexity" : "4" \
            } \
        }'
    }

    r2 = client.post(url, data=data)
    response = r2.json['challenge']

    assert r.status_code == 200
    assert r2.status_code == 409
    assert response == 'source_code already exists'

def test_post_code_not_compiles1(client):
    url = '/ruby/challenge'
    data = {
        'source_code_file': open('tests/ruby/tests-data/example_not_compile8.rb', 'rb'),
        'test_suite_file': open('tests/ruby/tests-data/example_test8.rb', 'rb'),
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "example8", \
                "test_suite_file_name" : "example_test8", \
                "repair_objective" : "Testing Compilation error", \
                "complexity" : "4" \
            } \
        }'
    }

    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 400
    assert response == 'source_code and/or test_suite not compile'

def test_post_code_not_compiles2(client):
    url = '/ruby/challenge'
    data = {
        'source_code_file': open('tests/ruby/tests-data/example8.rb', 'rb'),
        'test_suite_file': open('tests/ruby/tests-data/example_not_compile_test8.rb', 'rb'),
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "example8", \
                "test_suite_file_name" : "example_test8", \
                "repair_objective" : "Testing Compilation error", \
                "complexity" : "4" \
            } \
        }'
    }

    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 400
    assert response == 'source_code and/or test_suite not compile'

def test_post_bad_dependencies(client):
    url = '/ruby/challenge'
    data = {
        'source_code_file': open('tests/ruby/tests-data/example8.rb', 'rb'),
        'test_suite_file': open('tests/ruby/tests-data/example_dependencies_not_okay_test8.rb', 'rb'),
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "example8", \
                "test_suite_file_name" : "example_test8", \
                "repair_objective" : "Testing dependencies error", \
                "complexity" : "5" \
            } \
        }'
    }

    r = client.post(url, data=data)
    response = r.json['challenge']

    assert r.status_code == 400
    assert response == 'test_suite dependencies are wrong'