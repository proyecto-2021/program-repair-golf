import os
import pytest
from app import create_app, db
from . import client
#from app.cSharp.models import CSharp_Challenge


def test_post_challenge(client):
    #method to implement
    pass



def create_challenge(code_name=None, tests_name=None, repair_objective=None, complexity=None, code=None, tests_code=None):
    #method to implement
    pass


def challenge_json(dic_data):
    json_dic = '{ "challenge": { '
    if dic_data[next(iter(dic_data))] is not None:
        first_key = list(dic_data)[0]
    for key in dic_data:
        if dic_data[key] is not None:
            if key == first_key:
                json_dic += f'"{key}" : "{dic_data[key]}"'
            else:
                json_dic += f', "{key}" : "{dic_data[key]}"'

    json_dic += ' } }'
    return {'challenge': json_dic}

