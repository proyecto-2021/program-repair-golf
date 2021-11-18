import json
from flask import jsonify, request, make_response, json
from app import db
from . import go
from .models_go import GoChallenge
import os, subprocess, math, nltk, shutil
from .go_challenge_dao import goChallengeDAO
from .go_src import Go_src
from .go_controller import Controller


dao = goChallengeDAO()
controller = Controller()


@go.route('api/v1/go-challenges/<int:id>/repair', methods=['POST'])
def repair_challenge_go(id):
    return controller.post_repair(id)

@go.route('/api/v1/go-challenges', methods=['GET'])
def get_challenges():
    return controller.get_all_challenges()

@go.route('/api/v1/go-challenges/<id>', methods=['GET'])
def get_challenge(id):
    return controller.get_challenge_by_id(id)

@go.route('/api/v1/go-challenges/<id>', methods=['PUT'])
def update_a_go_challenge(id):
    return controller.update_a_go_challenge(id)
    
@go.route('/api/v1/go-challenges', methods=['POST'])
def create_go_challenge():
    return controller.post_challenge()


def from_file_to_str(challenge, attribute):
    file= open(str(os.path.abspath(challenge[attribute])),'r')
    content=file.readlines()
    file.close()
    challenge[attribute]=content
    return challenge

def compiles(commands, path):
    return (subprocess.run(commands, cwd=path, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL).returncode == 0)

def compiles(command):
    return (subprocess.call(command, shell=True, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL) == 0)

def content(path):
    f = open(path, 'r')
    return f.read()

def rewrite_file(path_to_file_used_to_update, path_to_file_to_update):
    with open(path_to_file_used_to_update) as file_used_to_update:
            with open(path_to_file_to_update, 'w') as file_to_update:
                for line in file_used_to_update:
                    file_to_update.write(line)

def delete_files(path):
    for file in os.listdir(path):
      os.remove(os.path.join(path, file))