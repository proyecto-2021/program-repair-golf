from . import cSharp
from app import db
from .models import CSharp_Challenge
from flask import jsonify, make_response

@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('/c-sharp-challenges/<int:id>', methods = ['GET'])
def get_challenge(id):
    if db.session.query(CSharp_Challenge).get(id) is None:
        return make_response(jsonify({'Challenge': 'Not found'}), 404)
    else:
        challenge = db.session.query(CSharp_Challenge).get(id).__repr__()
        challenge['code'] = open(challenge['code'], "r").read()
        challenge['tests_code'] = open(challenge['tests_code'], "r").read()
        return jsonify({ 'Challenge': challenge })


