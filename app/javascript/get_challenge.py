from flask import jsonify, make_response,request
from .. import db
from .models_js import JavascriptChallenge
from ..javascript import files_controller
from .folders_and_files import CODES_FOLDER 

def get_challenge_js(id):
  challenge = JavascriptChallenge.find_challenge(id)
  if not challenge: 
    return make_response(jsonify({"challenge":"Not found: challenge no exits"}), 404)

  challenge.code = files_controller.open_file(challenge.code)
  challenge.tests_code = files_controller.open_file(challenge.tests_code)
  challenge_dict = challenge.to_dict()
  del challenge_dict['id']
  
  return make_response(jsonify({"challenge": challenge_dict}), 200) 