from flask import jsonify, make_response,request
from .. import db
from .models_js import JavascriptChallenge
from ..javascript import files_js

def get_challenge_js(id):
  challenge = JavascriptChallenge.find_challenge(id)
  if not challenge: 
    return make_response(jsonify({"challenge":"Not found: challenge no exits"}), 404)

  print(challenge.code) 
  file_code = files_js.open_file(challenge.code) if files_js.exist_file(files_js.get_name_file( challenge.code)) else ""
  
  file_tests = files_js.open_file(challenge.tests_code) if files_js.exist_file(files_js.get_name_file(challenge.tests_code)) else ""

  if not file_code or not file_tests:
    return make_response(jsonify({"challenge":"Not found: file empty"}), 404)

  challenge_dict = challenge.to_dict()
  del challenge_dict['id']
  challenge_dict['code'] = file_code
  challenge_dict['tests_code'] =file_tests

  return make_response(jsonify({"challenge": challenge_dict}), 200) 