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
    challenge= CSharp_Challenge.query.filter_by(id=id).first()
    data_Challenge = loads(request.form.get('challenge'))['challenge']

    if challenge is None:
        return make_response(jsonify({"challenge":"There is no challenge for this id"}), 404)



