import json
from flask import jsonify, request, make_response, json
from app import db
from . import go
from .models_go import GoChallenge
import os, subprocess, math, nltk, shutil
from .go_controller import Controller
from flask_jwt import jwt_required

controller = Controller()

@go.route('api/v1/go-challenges/<int:id>/repair', methods=['POST'])
@jwt_required()
def repair_challenge_go(id):
    return controller.post_repair(id)

@go.route('/api/v1/go-challenges', methods=['GET'])
@jwt_required()
def get_challenges():
    return controller.get_all_challenges()

@go.route('/api/v1/go-challenges/<id>', methods=['GET'])
@jwt_required()
def get_challenge(id):
    return controller.get_challenge_by_id(id)

@go.route('/api/v1/go-challenges/<id>', methods=['PUT'])
@jwt_required()
def update_a_go_challenge(id):
    return controller.update_a_go_challenge(id)
    
@go.route('/api/v1/go-challenges', methods=['POST'])
@jwt_required()
def create_go_challenge():
    return controller.post_challenge()
    