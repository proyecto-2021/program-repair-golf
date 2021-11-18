from os import makedev
from flask.helpers import make_response
from app.java.controller import *
from . import java
from app import db
from flask import Flask, request, jsonify, json
from json import loads
from flask_jwt import jwt_required, current_identity

@java.route('/java-challenges',methods=['GET'])
@jwt_required()
def ViewAllChallenges():
    try:
        output = controller.list_challenges_java()
    except Exception as e:
        return make_response(jsonify(str(e)), 404)
    return make_response(jsonify({"challenges": output}))
    
@java.route('/java-challenges/<int:id>',methods=['GET'])
@jwt_required()
def View_Challenges(id):
    try:
       output = controller.challenges_id_java(id)
    except Exception as e:
        return make_response(jsonify(str(e)), 404)
    return make_response(jsonify({"challenge": output}))
    
@java.route('/java-challenges/<int:id>', methods=['PUT'])
@jwt_required()
def UpdateChallenge(id):
    try:
        output= controller.challenge_upd_java(id)
    except Exception as e:
                return make_response(jsonify(str(e)), 404)
    return make_response(jsonify({"challenge": output}))
   
@java.route('/java-challenges', methods=['POST'])
@jwt_required()
def create_challenge():
    try:
        output = controller.add_challenge_java()
    except Exception as e:
        return make_response(jsonify(str(e)), 404)
    return make_response(jsonify({"challenge": output}), 200)

@java.route('/java-challenges/<int:id>/repair', methods=['POST'])
@jwt_required()
def repair_challenge(id):
    try:
        output = controller.repair_file(id)
    except Exception as e:
        return make_response(jsonify(str(e)), 404)
    return make_response(jsonify(output))

