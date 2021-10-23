from . import client

def test_post_challenge(client):
    url = '/ruby/challenge'
    data = {
        'source_code_file': open('tests/ruby/test-files/example.rb','rb'),
        'test_suite_file': open('tests/ruby/test-files/example_test.rb','rb'),
        'challenge': '{ \
            "challenge": { \
                "source_code_file_name" : "example", \
                "test_suite_file_name" : "example_test", \
                "repair_objective" : "Testing", \
                "complexity" : "2" \
            } \
        }'
    }

    r = client.post(url, data=data)
    assert r.status_code == 200
    assert r.json == {
                    "challenge": {
                            "id": 1,
                            "code": "public/challenges/example.rb",
                            "tests_code": "public/challenges/example_test.rb",
                            "repair_objective": "Testing",
                            "complexity": "2",
                            "best_score": 0
                        }
                    }
