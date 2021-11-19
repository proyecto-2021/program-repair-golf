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
    update_request = {}
    update_request['source_code_file'] = request.files.get('source_code_file')
    update_request['test_suite_file'] = request.files.get('test_suite_file')
    update_request['challenge'] = request.form.get('challenge')
    if update_request['challenge'] is not None:
        update_request['challenge'] = json.loads(update_request['challenge'])
        update_request['challenge'] = update_request['challenge']['challenge']


    challenge = DAO.get_challenge_db(id)
    if not DAO.exist(id):
        return make_response(jsonify({"challenge": "There is no challenge for this id"}), 404)
    files_keys = ("source_code_file", "test_suite_file")

    challenge_name = os.path.basename(challenge['code'])
    test_name = os.path.basename(challenge['tests_code'])
    challenge_exe = challenge_name.replace('.cs', '.exe')
    test_dll = test_name.replace('.cs', '.dll')
    challenge_dir = DAO.CHALLENGE_SAVE_PATH + challenge_name.replace('.cs', '/')
    old_challenge_path = challenge_dir + challenge_name
    old_test_path = challenge_dir + test_name
    new_challenge_path = DAO.CHALLENGE_VALIDATION_PATH + challenge_name
    new_test_path = DAO.CHALLENGE_VALIDATION_PATH + test_name
    new_challenge_exe_path = DAO.CHALLENGE_VALIDATION_PATH + challenge_exe
    new_test_dll_path = DAO.CHALLENGE_VALIDATION_PATH + test_dll
    new_challenge = update_request['source_code_file']
    new_test = update_request['test_suite_file']

    if new_challenge is not None and new_test is not None:
        new_ch = CSharpChallenge(new_challenge,
                                 new_test,
                                 challenge_name,
                                 test_name,
                                 new_challenge_path,
                                 new_test_path)
        val_status = new_ch.validate()
        DAO.handle_put_files(val_status, old_challenge_path,
                             old_test_path, new_ch.code.path,
                             new_ch.test.path)
        if val_status != 1:
            return code_validation_response(val_status)
    elif new_challenge is not None:
        new_ch = CSharpChallenge(new_challenge,
                                 open(old_test_path, "rb"),
                                 challenge_name,
                                 test_name,
                                 new_challenge_path,
                                 old_test_path)
        val_status = new_ch.validate()
        DAO.handle_put_files(val_status, old_challenge_path, new_ch.test.path,
                             new_ch.code.path)
        if val_status != 1:
            return code_validation_response(val_status)
    elif new_test is not None:
        new_ch = CSharpChallenge(open(old_challenge_path, "rb"),
                                 new_test,
                                 challenge_name,
                                 test_name,
                                 old_challenge_path,
                                 new_test_path)
        val_status = new_ch.validate()
        DAO.handle_put_files(val_status, new_ch.code.path, old_test_path,
                             test_path=new_ch.test.path)
        if val_status != 1:
            return code_validation_response(val_status)

    if update_request['challenge'] is not None:
        if 'repair_objective' in update_request['challenge']:
            DAO.update_challenge_data(id, {'repair_objective': update_request['challenge']['repair_objective']})

        if 'complexity' in update_request['challenge']:
            complexity = int(update_request['challenge']['complexity'])
            if complexity < 1 or complexity > 5 :
                return make_response(jsonify({'Complexity': 'Must be between 1 and 5'}), 409)
            else:
                DAO.update_challenge_data(id, {'complexity': complexity})
    return make_response(jsonify({'challenge': DAO.get_challenge_db(id, show_files_content=True)}), 200)

  
@cSharp.route('/c-sharp-challenges', methods=['POST'])
def post_csharp_challenges():
    # Get new challenge data
    try:
        new_challenge = loads(request.form.get('challenge'))['challenge']
        new_challenge['source_code_file'] = request.files['source_code_file']
        new_challenge['test_suite_file'] = request.files['test_suite_file']
    except Exception:
        return make_response(jsonify({"challenge": "Data not found"}), 404)
    finally:
        if 'source_code_file' not in new_challenge or 'test_suite_file' not in new_challenge:
            return make_response(jsonify({"challenge": "Data not found"}), 404)

    # Validate challenge data
    required_keys = ('source_code_file_name', 'test_suite_file_name',
                     'source_code_file', 'test_suite_file',
                     'repair_objective', 'complexity')
    if all(key in new_challenge for key in required_keys):
        try:
            ch_dir = DAO.create_challenge_dir(new_challenge['source_code_file_name'])
        except FileExistsError:
            return make_response(jsonify({'Challenge': 'Already exists'}), 409)
        new_source_code_path = ch_dir + new_challenge['source_code_file_name'] + ".cs"
        new_test_suite_path = ch_dir + new_challenge['test_suite_file_name'] + ".cs"
        challenge = CSharpChallenge(new_challenge['source_code_file'],
                                    new_challenge['test_suite_file'],
                                    new_challenge['source_code_file_name'],
                                    new_challenge['test_suite_file_name'],
                                    new_source_code_path,
                                    new_test_suite_path)
        validate_response = challenge.validate()
        new_code_exe_path = challenge.code.path.replace('.cs', '.exe')
        new_test_dll_path = challenge.test.path.replace('.cs', '.dll')
        if validate_response == 0:
            DAO.remove_challenge_dir(new_challenge['source_code_file_name'])
            return make_response(jsonify({'Test': 'At least one has to fail'}), 409)

        elif validate_response == 1:
            DAO.remove(new_code_exe_path, new_test_dll_path)
            complexity = int(new_challenge['complexity'])
            if complexity < 1 or complexity > 5:
                DAO.remove_challenge_dir(new_challenge['source_code_file_name'])
                return make_response(jsonify({'Complexity': 'Must be between 1 and 5'}), 409)
            new_data_id = DAO.save_to_db(new_challenge['repair_objective'],
                                         complexity,
                                         challenge.code.file_name,
                                         challenge.test.file_name)
            content = DAO.get_challenge_db(new_data_id, show_files_content=True)
            return make_response(jsonify({'challenge': content}))

        elif validate_response == 2:
            DAO.remove_challenge_dir(new_challenge['source_code_file_name'])
            return make_response(jsonify({'Test': 'Sintax errors'}), 409)

        else:
            DAO.remove_challenge_dir(new_challenge['source_code_file_name'])
            return make_response(jsonify({'Challenge': 'Sintax errors'}), 409)

    else:
        return make_response(jsonify({'challenge': 'Data not found'}), 404)


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


def code_validation_response(val_status):
    if val_status == -1:
        return make_response(jsonify({'Source code': 'Sintax errors'}), 409)
    elif val_status == 0:
        return make_response(jsonify({'Challenge': 'Must fail at least one test'}), 409)
    elif val_status == 2:
        return make_response(jsonify({'Test': 'Sintax errors'}), 409)
