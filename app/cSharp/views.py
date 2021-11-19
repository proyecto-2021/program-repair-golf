from posixpath import basename
from . import cSharp
from .c_sharp_challenge import CSharpChallenge
from .c_sharp_repair_candidate import CSharpRepairCandidate
from .c_sharp_challenge_DAO import CSharpChallengeDAO
from json import loads
from flask import jsonify, make_response, json, request
from .c_sharp_controller import CSharpController
import os

DAO = CSharpChallengeDAO()
controller = CSharpController()

@cSharp.route('/login')
def login():
    return {'result': 'Ok'}


@cSharp.route('/c-sharp-challenges/<int:id>', methods=['PUT'])
def put_csharp_challenges(id):
    return controller.update_challenge(id,request.files.get('source_code_file'),
                                       request.files.get('test_suite_file'),
                                       request.form.get('challenge'))

@cSharp.route('/c-sharp-challenges', methods=['POST'])
def post_csharp_challenges():
    return controller.post_challenge(request.files.get('source_code_file'),
                                     request.files.get('test_suite_file'),
                                     request.form.get('challenge'))


@cSharp.route('c-sharp-challenges/<int:id>/repair', methods=['POST'])
def repair_candidate(id):
    return controller.post_repair_candidate(id,request.files.get('source_code_file'))


@cSharp.route('/c-sharp-challenges/<int:id>', methods=['GET'])
def get(id):
    return controller.get_challenge(id)


@cSharp.route('/c-sharp-challenges', methods=['GET'])
def get_csharp_challenges():
    challenge = {'challenges': []}
    show = []
    challenge['challenges'] = DAO.get_all_challenges()
    for i in challenge['challenges']:
        show.append(DAO.get_challenge_db(i.__repr__()['id'],
                                         show_files_content=True))
    if show != []:
        return jsonify({'challenges': show})
    else:
        return jsonify({'challenges': 'None Loaded'})

