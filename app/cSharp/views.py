from . import cSharp
from app import db
from .models import CSharp_Challenge
from  flask import jsonify,make_response,json,request
import subprocess,os


@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('c-sharp-challenges/<int:id>/repair', methods=['POST'])
def repair_Candidate(id):
    #to do : implement this method
    # verify challenge's existence 
    if db.session.query(CSharp_Challenge).get(id) is not None:
        challenge = db.session.query(CSharp_Challenge).get(id).__repr__()
        if os.path.exists(request.get_json()['source_code_file']):
            with open(request.json('source_code_file'),'r') as repair_file:
                # check if repair candidate passes test. If this happens then calculate score.
                pass
        else:
            return make_response(jsonify({'repair challenge': 'Not found'}),404)
    else: 
        return make_response(jsonify({'challenge': 'Not found'}),404)
    pass
