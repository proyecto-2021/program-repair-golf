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
def repair_Candidate(id):
    # verify challenge's existence
    if DAO.exist(id):
        challenge = DAO.get_challenge_db(id)
        challenge_name = os.path.basename(challenge['code'])
        test_name = os.path.basename(challenge['tests_code'])
        try:
            file = request.files['source_code_file']
        except Exception:
            return make_response(jsonify({'Repair candidate': 'Not found'}), 404)
        repair_path = DAO.CHALLENGE_VALIDATION_PATH + challenge_name
        challenge_to_repair = CSharpChallenge(open(challenge['code'], "rb"), open(challenge['tests_code'], "rb"),
                                              challenge_name, test_name, challenge['code'], 
                                              challenge['tests_code'])
        repair = CSharpRepairCandidate(challenge_to_repair,file,challenge_name,repair_path)
        validation_result = repair.validate()
        if validation_result == -1:
            DAO.remove(repair.code.path)
            return make_response(jsonify({'Repair candidate': 'Sintax error'}), 409)

        elif validation_result == 1:
            DAO.remove(repair.code.path)
            DAO.remove(repair.code.path.replace('.cs', '.exe'),
                       repair.challenge.test.path.replace(".cs", ".dll"))
            return make_response(jsonify({'Repair candidate': 'Tests not passed'}), 409)
        else:
            score = repair.score()

            if DAO.save_best_score(score, challenge['best_score'], id) == 0:
                challenge['best_score'] = score

            challenge_data = {
                "repair_objective": challenge['repair_objective'],
                "best_score": challenge['best_score']
            }
            DAO.remove(repair.code.path)
            DAO.remove(repair.code.path.replace('.cs', '.exe'),
                       repair.challenge.test.path.replace(".cs", ".dll"))
            return make_response(jsonify({'Repair': {'challenge': challenge_data, 'score': score}}), 200)
    else:
        return make_response(jsonify({"challenge": "There is no challenge for this id"}), 404)


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

