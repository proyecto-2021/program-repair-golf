from flask.helpers import make_response
from app.java import *
from app.java.controller import *
from . import java
from app import db
from flask import Flask, request, jsonify, json
from json import loads
import nltk
from app.java.challenge_candidate import ChallengeCandidate

UPLOAD_FOLDER = './public/challenges/'
PATHLIBRERIA = 'app/java/lib/junit-4.13.2.jar:public/challenges'
PATHEXECUTE = 'org.junit.runner.JUnitCore'
ALLOWED_EXTENSIONS = {'java'}
EJECUTARFILE= 'app/java/lib/hamcrest-all-1.3.jar:app/java/lib/junit-4.13.2.jar:public/challenges/'

@java.route('/prueba')
def login():
    return { 'result': 'funciona' }

@java.route('/java-challenges',methods=['GET'])
def ViewAllChallenges():
    return controller.list_challenges_java()
    
@java.route('/java-challenges/<int:id>',methods=['GET'])
def View_Challenges(id):
    return controller.challenges_id_java(id)
    
@java.route('/java-challenges/<int:id>', methods=['PUT'])
def UpdateChallenge(id):
    return controller.challenge_upd_java(id)

@java.route('/java-challenges', methods=['POST'])
def create_challenge():
   return controller.add_challenge_java()

@java.route('/java-challenges/<int:id>/repair', methods=['POST'])
def repair_challenge(id):
    return controller.repair_file(id)

