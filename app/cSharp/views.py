from . import cSharp
from . import cSharp
from app import db
from .models import CSharp_Challenge
from flask import jsonify


@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }



@cSharp.route('/c-sharp-challenges', methods=['POST'])
def post_csharp_challenges():
    #[TODO]: implement this method
    return {'challenges': 'Unsupported View'}

