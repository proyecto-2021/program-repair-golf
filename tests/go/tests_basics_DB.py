from app import create_app, db
import pytest
from app.go.models_go import GoChallenge
from . import client

def add_new_challenge():
	challenge=GoChallenge(code="path",tests_code="test_path",repair_objective="repair",complexity="coplexity",best_score=100)
	db.session.add(challenge)
	db.session.commit()
	return challenge.id


def test_get_all_challenges_go(client):
	for i in range(0,8):
			add_new_challenge()
	list_of_challenges=GoChallenge.query.all()
	assert len(list_of_challenges)==8

def test_add_a_new_challenge(client):
	i=add_new_challenge()
	challenge=GoChallenge.query.all()
	assert len(challenge)==9
	assert challenge[8].id==i


def test_get_challenge_go(client):
	id=add_new_challenge()
	challenge= GoChallenge.query.filter_by(id=id).first()
	assert (challenge is None) == False

def test_update_challenge_go(client):
	id=add_new_challenge()
	challenge= GoChallenge.query.filter_by(id=id).first()
	challenge.code="changed"
	db.session.commit()
	challenge= GoChallenge.query.filter_by(code="changed").first()
	assert (challenge is None) == False

