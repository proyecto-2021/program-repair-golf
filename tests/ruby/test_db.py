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
    )

    return challenge

def test_create_challenge(client):
    RubyChallenge.create_challenge('code', 'tests_code', 'repair_objective', '5')
    assert len(RubyChallenge.query.all()) == 1

def test_get_challenge(client):
    challenge = RubyChallenge.create_challenge('code', 'tests_code', 'repair_objective', '5')
    assert challenge['id'] == 2

def test_get_all_challenges(client):
    challenges_list = RubyChallenge.get_challenges()
    assert len(challenges_list) == 2
    
    for i in range(10):
        RubyChallenge.create_challenge('code', 'tests_code', 'repair_objective', '5')
    
    challenges_list = RubyChallenge.get_challenges()
    assert len(challenges_list) == 12
    
    
    
    
    
    
    
    
     
    


