from . import cSharp
from app import db
from .models import CSharp_Challenge
from flask import jsonify

@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('/c-sharp-challenges/<int:id>', methods = ['GET'])
def get_challenge(id):
    challenge = db.session.query(CSharp_Challenge).get(id).__repr__()
    return jsonify({ 'Challenge': challenge })

