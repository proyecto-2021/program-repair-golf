import random
import string
import pytest
from . import client
from app.ruby.models.rubychallengedao import RubyChallengeDAO

def get_tests_data(n):
    tests_data_list = []
    for _ in range(n):
        data = dict()
        data['code'] = str(random.choices(string.ascii_letters + string.digits,k=10))
        data['tests_code'] = str(random.choices(string.ascii_letters + string.digits,k=10))
        data['repair_objective'] = str(random.choices(string.ascii_letters + string.digits,k=10))
        data['complexity'] = str(random.randint(1,5))
        tests_data_list.append(data)
    return tests_data_list

@pytest.mark.parametrize("data", get_tests_data(5))
def test_create_challenge(client, data):
    dao = RubyChallengeDAO()
    id = dao.create_challenge(**data)

    assert id is not None

@pytest.mark.parametrize("data", get_tests_data(5))
def test_get_one_after_create(client, data):
    dao = RubyChallengeDAO()
    id = dao.create_challenge(**data)

    challenge = dao.get_challenge(id)
    del challenge['best_score']

    assert challenge == data

@pytest.mark.parametrize("data", get_tests_data(5))
def test_get_all_after_create(client, data):
    dao = RubyChallengeDAO()
    list1 = dao.get_challenges()

    dao.create_challenge(**data)
    list2 = dao.get_challenges()

    assert len(list1) == len(list2) - 1

@pytest.mark.parametrize("data", get_tests_data(5))
def test_check_existence_after_create(client, data):
    dao = RubyChallengeDAO()
    id = dao.create_challenge(**data)

    assert dao.exists(id)

@pytest.mark.parametrize("data1,data2", zip(get_tests_data(5), get_tests_data(5)))
def test_update_after_create(client, data1, data2):
    dao = RubyChallengeDAO()
    id = dao.create_challenge(**data1)
    challenge1 = dao.get_challenge(id)
    data1['best_score'] = 0

    data2['best_score'] = random.randint(1,100)
    dao.update_challenge(id, data2)
    challenge2 = dao.get_challenge(id)

    assert challenge1 == data1
    assert challenge2 == data2
