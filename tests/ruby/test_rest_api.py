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
                            "code": "def median(a,b,c)\n  "
                                        "res = 0\n  "
                                        "if ((a>=b and a<=c) or (a>=c and a<=b))\n    "
                                            "res = a\n  "
                                        "end\n  "
                                        "if ((b>=a and b<=c) or (b>=c and b<=a))\n    "
                                            "res = b\n  "
                                        "else\n    "
                                            "res = c\n  "
                                        "end\n  "
                                        "return res\n"
                                    "end\n",
                            "tests_code":   "require 'minitest/autorun'\n"
                                            "require_relative 'example'\n"
                                            "\n"
                                            "class MedianTest < Minitest::Test\n  "
                                                "def test_1\n    "
                                                    "assert median(1,2,3) == 2\n  "
                                                "end\n"
                                                "\n  "
                                                "def test_2\n    "
                                                    "assert median(2,1,3) == 2\n  "
                                                "end\n"
                                                "\n  "
                                                "def test_3\n    "
                                                    "assert median(3,1,2) == 2\n  "
                                                "end\n"
                                            "end\n",
                            "repair_objective": "Testing",
                            "complexity": "2",
                            "best_score": 0
                        }
                    }
