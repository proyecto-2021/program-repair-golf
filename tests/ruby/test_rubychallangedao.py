from app.ruby.models.rubychallengedao import RubyChallengeDAO
from . import client
import random
import string
import pytest


def get_tests_data(n):
    tests_data_list = []
    for _ in range(n):
        data = dict()
        data['code'] = str(random.choices(string.ascii_letters + string.digits, k=10))
        data['tests_code'] = str(random.choices(string.ascii_letters + string.digits, k=10))
        data['repair_objective'] = str(random.choices(string.ascii_letters + string.digits, k=10))
        data['complexity'] = str(random.randint(1, 5))
        tests_data_list.append(data)
    return tests_data_list


@pytest.mark.parametrize("data", get_tests_data(5))
def test_create_challenge(client, data):
    # arrange
    dao = RubyChallengeDAO()

    # act
    challenge_id = dao.create_challenge(**data)

    # assert
    assert challenge_id is not None


@pytest.mark.parametrize("data", get_tests_data(5))
def test_get_one_after_create(client, data):
    # arrange
    dao = RubyChallengeDAO()
    challenge_id = dao.create_challenge(**data)

    # act
    challenge = dao.get_challenge(challenge_id)
    del challenge['best_score']

    # assert
    assert challenge == data


@pytest.mark.parametrize("data", get_tests_data(5))
def test_get_all_after_create(client, data):
    # arrange
    dao = RubyChallengeDAO()
    list1 = dao.get_challenges()
    challenge_id = dao.create_challenge(**data)

    # act
    challenge = dao.get_challenge(challenge_id)
    challenge['id'] = challenge_id
    list2 = dao.get_challenges()

    # assert
    assert len(list1) == len(list2) - 1
    assert challenge in list2


@pytest.mark.parametrize("data", get_tests_data(5))
def test_check_existence_after_create(client, data):
    # arrange
    dao = RubyChallengeDAO()

    # act
    challenge_id = dao.create_challenge(**data)

    # assert
    assert dao.exists(challenge_id)


@pytest.mark.parametrize("data1,data2", zip(get_tests_data(5), get_tests_data(5)))
def test_update_after_create(client, data1, data2):
    # arrange
    dao = RubyChallengeDAO()
    challenge_id = dao.create_challenge(**data1)
    challenge1 = dao.get_challenge(challenge_id)
    data1['best_score'] = 0
    data2['best_score'] = random.randint(1, 100)

    # act
    dao.update_challenge(challenge_id, data2)
    challenge2 = dao.get_challenge(challenge_id)

    # assert
    assert challenge1 == data1
    assert challenge2 == data2
