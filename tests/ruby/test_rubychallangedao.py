import random
import string
import pytest
from . import client
from app.ruby.rubychallengedao import RubyChallengeDAO

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