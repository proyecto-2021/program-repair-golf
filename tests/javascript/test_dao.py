import pytest

from . import client
from app.javascript.models_js import *
from app.javascript.dao.challenge_dao import ChallengeDAO 

def test_get_all_challenges(client):
    empty_list = ChallengeDAO.get_all_challenges()
    assert empty_list == []   