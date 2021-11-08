from app import create_app, db
import pytest
from app.java.models_java import *
from . import client
from app.java.views import *

#Create Challenge
#def test_new_challenge(client):

def test_ViewAllChallenges(client):
    #elegir entradas para test
    challenge = {"challenges":[]}
    #ejecutar dichas entrada
    challenge ['challenges'] = ViewAllChallenges()
    resp = len(challenge)
    #verificar el comportamiento esperado
    if resp >= 1:
        assert resp !=0
    else:
        assert resp == 0
   
def test_ViewChallenges(client):
    challenge = {"challenges":[]}
    id=1
    challenge ['challenges'] = View_Challenges(id)
    resp = len(challenge)
    assert resp == 1 
