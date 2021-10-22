from app import create_app, db
import pytest
from app.ruby.models import RubyChallenge
from . import client

def generate_challenge():
    challenge = RubyChallenge(
        code='code',
        tests_code='tests_code',
        repair_objective='repair_objective',
        complexity='5',
        best_score=0
    )
    
    return challenge

def test_create_challenge(client):
    challenge = generate_challenge()
    RubyChallenge.create_challenge(challenge)

    assert len(RubyChallenge.query.all()) == 1

def test_get_challenge(client):
    challenge1 = RubyChallenge.get_challenge(1)
    RubyChallenge.create_challenge(generate_challenge())
    challenge2 = RubyChallenge.get_challenge(2)

    assert challenge1.get_dict()['id'] == 1
    assert challenge2.get_dict()['id'] == 2

def test_get_all_challenges(client):
    challenges_list = RubyChallenge.get_challenges()
    assert len(challenges_list) == 2
    
    for i in range(10):
        RubyChallenge.create_challenge(generate_challenge())
    
    challenges_list = RubyChallenge.get_challenges()
    assert len(challenges_list) == 12
    
    
    
    
    
    
    
    
     
    


