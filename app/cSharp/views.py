from . import cSharp
from app import db
from .models import CSharp_Challenge
from  flask import jsonify,make_response,json,request

@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('c-sharp-challenges/<int:id>/repair', methods=['POST'])
def repair_Candidate(id):
    #to do : implement this method
    # verify challenge's existence 
    if db.session.query(CSharp_Challenge).get(id) is not None:
        archivo = open(request.json('source_code_file'),'r')
        # check if repair candidate passes test. If this happens then calculate score.
    else: 
        return make_response(jsonify({'challenge': 'Not found'}),404)
    pass
