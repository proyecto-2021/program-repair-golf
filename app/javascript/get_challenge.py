from flask import jsonify, make_response,request
from .. import db
from .models_js import JavascriptChallenge
from .controllers.files_controller import open_file, exist_file
from .folders_and_files import CODES_FOLDER 
from .exceptions.HTTPException import HTTPException

def get_challenge_js(id):
  
  challenge = JavascriptChallenge.find_challenge(id)
  if not challenge: 
    return make_response(jsonify({"challenge":"Not found: challenge no exits"}), 404)

  challenge.code = open_file(challenge.code)
  challenge.tests_code = open_file(challenge.tests_code)
  challenge_dict = challenge.to_dict()
  del challenge_dict['id']

  return make_response(jsonify({"challenge": challenge_dict}), HTTPException.HTTP_OK)
