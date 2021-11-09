from app import create_app, db
import pytest
from app.java.models_java import *
from . import client
from app.java.views import *

#Create Challenge
#def test_new_challenge(client):
def test_ViewAllChallenges(client):
    challenge = {"challenges":[]}
    challenge ['challenges'] = DAO_java_challenge.all_challenges_java()
    resp = len(challenge)
    assert resp == 1

    #verrrrrrrrrrrrrrrrrrrrrrrrrrrr 
    '''
    dict={"dict":[]}
    dict['source_code_file_name']='source_code_file_name'
    dict['test_suite_file_name']='test_suite_file_name'
    dict['repair_objective']='repair_objective'
    dict['complexity']='complexity'
    dict['score']=500
    DAO_java_challenge.create_challenge(dict)
    resp = len(challenge)
    challenge ['challenges'] = DAO_java_challenge.all_challenges_java()
    assert resp == 2
    '''

def test_ViewChallenges(client):
    challenge = {"challenges":[]}
    id=1
    challenge ['challenges'] = DAO_java_challenge.challenges_id_java(id)
    resp = len(challenge)
    assert resp == 1 
