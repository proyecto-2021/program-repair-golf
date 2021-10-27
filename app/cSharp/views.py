from . import cSharp
from . import cSharp
from app import db
from .models import CSharp_Challenge
from flask import jsonify, request, make_response
from json import loads
import os  

CHALLENGE_SAVE_PATH = "example-challenges/c-sharp-challenges/"

@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('/c-sharp-challenges', methods=['POST'])
def post_csharp_challenges():
    new_challenge = loads(request.form.get('challenge'))['challenge']

    #Validate challenge data
    
    try:
        os.mkdir(CHALLENGE_SAVE_PATH, new_challenge['source_code_file_name'])
    except FileExistsError:
        return make_response(jsonify({'Challenge': 'Already exists'}), 409)
    
    #Save validated data
    
    return make_response(jsonify({'Method': 'Not implemented'}), 405)

