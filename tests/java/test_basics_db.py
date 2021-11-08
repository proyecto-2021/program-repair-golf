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
    challenge = Challenge_java(code='source_code_file_name', tests_code='test_suite_file_name', repair_objective='repair_objective', complexity='complexity', score=500)
    for j in range (5):  
        DAO_java_challenge.create_challenge(challenge)
    challenge ['challenges'] = DAO_java_challenge.all_challenges_java()
    assert resp == 6
    '''

def test_ViewChallenges(client):
    challenge = {"challenges":[]}
    id=1
    challenge ['challenges'] = DAO_java_challenge.challenges_id_java(id)
    resp = len(challenge)
    assert resp == 1 
