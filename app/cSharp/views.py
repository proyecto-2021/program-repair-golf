from . import cSharp
from app import db
from .models import CSharp_Challenge
from flask import jsonify
from flask import make_response

@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('/c-sharp-challenges/<int:id>', methods=['PUT'])
def put_csharp_challenges():
    #[TODO]: implement this method
    return {'challenges': 'Unsupported View'}
