from . import client, auth, generic_post
from nltk import edit_distance


def test_post_repair1(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    url = f'/ruby/challenge/{challenge_id}/repair'
    data = {'source_code_file': open('tests/ruby/tests-data/example_fixed1.rb', 'rb')}

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})
    with open('tests/ruby/tests-data/example_fixed1.rb') as f:
        code_fixed_content = f.read()

    # assert
    assert r.status_code == 200
    assert r.json['repair']['score'] == edit_distance(orig_json['code'], code_fixed_content)
    assert r.json['repair']['player']['username'] == 'ruby'


def test_post_repair2(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    url = f'/ruby/challenge/{challenge_id}/repair'
    data1 = {'source_code_file': open('tests/ruby/tests-data/example_fixed1.rb', 'rb')}
    data2 = {'source_code_file': open('tests/ruby/tests-data/example_not_compiles.rb', 'rb')}
    data3 = {'source_code_file': open('tests/ruby/tests-data/example_fixed2.rb', 'rb')}

    # act
    r1 = client.post(url, data=data1, headers={'Authorization': f'JWT {auth}'})
    with open('tests/ruby/tests-data/example_fixed1.rb') as f:
        code_fixed_content1 = f.read()

    r2 = client.post(url, data=data2, headers={'Authorization': f'JWT {auth}'})

    r3 = client.post(url, data=data3, headers={'Authorization': f'JWT {auth}'})
    with open('tests/ruby/tests-data/example_fixed2.rb') as f:
        code_fixed_content2 = f.read()

    # assert
    assert r1.status_code == 200
    assert r1.json['repair']['score'] == edit_distance(orig_json['code'], code_fixed_content1)
    assert r1.json['repair']['player']['username'] == 'ruby'
    assert r2.status_code == 400
    assert r2.json['challenge'] == 'the repair candidate has syntax errors'
    assert r3.status_code == 200
    assert r3.json['repair']['score'] == edit_distance(orig_json['code'], code_fixed_content2)
    assert r3.json['repair']['player']['username'] == 'ruby'
    assert str(int(r1.json['repair']['attempts']) + 2) == r3.json['repair']['attempts']


def test_post_repair_invalid_challenge(client, auth):
    # arrange
    url = '/ruby/challenge/1000/repair'  # its probably that we dont post 1000 challenges for test
    data = {'source_code_file': open('tests/ruby/tests-data/example_fixed1.rb', 'rb')}

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 404
    assert r.json['challenge'] == 'the id does not exist'


def test_post_repair_candidate_compiles_error(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    url = f'/ruby/challenge/{challenge_id}/repair'
    data = {'source_code_file': open('tests/ruby/tests-data/example_not_compiles.rb', 'rb')}

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'the repair candidate has syntax errors'


def test_post_repair_candidate_tests_fail(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    url = f'/ruby/challenge/{challenge_id}/repair'
    data = {'source_code_file': open('tests/ruby/tests-data/example_median.rb', 'rb')}

    # act
    r = client.post(url, data=data, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 200
    assert r.json['challenge'] == 'the repair candidate does not solve the problem'


def test_post_repair_without_repair_candidate(client, auth, generic_post):
    # arrange
    orig_json = generic_post['challenge'].copy()
    challenge_id = orig_json['id']
    url = f'/ruby/challenge/{challenge_id}/repair'

    # act
    r = client.post(url, headers={'Authorization': f'JWT {auth}'})

    # assert
    assert r.status_code == 400
    assert r.json['challenge'] == 'a repair candidate is necessary'


def test_post_repair_without_authentication(client):
    # arrange
    url = '/ruby/challenge/1000/repair'

    # act
    r = client.post(url)

    # assert
    assert r.status_code == 401
    assert r.json['error'] == 'Authorization Required'
