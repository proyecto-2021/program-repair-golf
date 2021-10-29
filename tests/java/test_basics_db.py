from app import create_app, db
import pytest
from app.java.models_java import *
from . import client


#Create Challenge
#def test_new_challenge(client):

def test_ViewAllChallenges(client):
    challenge = {"challenges":[]}
    challenge ['challenges'] = Challenge_java.query.all()
    # ViewAllChallenges() hacer...
    res = len(challenge)
    assert  res == 1
    #comportamiento esperado

   
