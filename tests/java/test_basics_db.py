from app import create_app, db
import pytest
from app.java.models_java import *
from . import client
from app.java.views import *

#Create Challenge
#def test_new_challenge(client):

def test_ViewAllChallenges(client):
    challenge = {"challenges":[]}
    challenge ['challenges'] = ViewAllChallenges()
    resp = len(challenge)
    if resp >= 1:
        assert resp !=0
   
