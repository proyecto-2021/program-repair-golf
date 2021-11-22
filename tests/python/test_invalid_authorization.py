from . import client, jwt_token
from .atest_utils import *
import json


# testing of one invalid post challenge
def test_post_pythonChallenge(client, jwt_token):
    repair_objective = "make to pass"
    jwt_token = None
    response = send_post(client, jwt_token, "valid_code_3.py", "valid_atest_3.py", repair_objective, "2", default_code_content=False)
    assert response.status_code == 401
