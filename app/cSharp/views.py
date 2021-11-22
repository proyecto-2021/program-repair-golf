from . import cSharp
from json import loads
from flask import request
from .c_sharp_controller import CSharpController
from flask_jwt import jwt_required

controller = CSharpController()

@cSharp.route('/c-sharp-challenges/<int:id>', methods=['PUT'])
@jwt_required()
def put_csharp_challenges(id):
    return controller.update_challenge(id,request.files.get('source_code_file'),
                                       request.files.get('test_suite_file'),
                                       request.form.get('challenge'))

  
@cSharp.route('/c-sharp-challenges', methods=['POST'])
@jwt_required()  
def post_csharp_challenges():
    # Get new challenge data
    try:
        new_challenge = loads(request.form.get('challenge'))['challenge']
        new_challenge['source_code_file'] = request.files.get('source_code_file')
        new_challenge['test_suite_file'] = request.files.get('test_suite_file')
    except Exception:
        return make_response(jsonify({"challenge": "Data not found"}), 404)
    keys_in_challenge = ('source_code_file_name',
                         'test_suite_file_name',
                         'complexity',
                         'repair_objective')
    if not all(key in new_challenge for key in keys_in_challenge):
        return make_response(jsonify({"challenge": "Data not found"}), 404)
           
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

    return controller.post_challenge(request.files.get('source_code_file'),
                                     request.files.get('test_suite_file'),
                                     request.form.get('challenge'))


@cSharp.route('c-sharp-challenges/<int:id>/repair', methods=['POST'])
@jwt_required()
def repair_candidate(id):
    return controller.post_repair_candidate(id,request.files.get('source_code_file'))


@cSharp.route('/c-sharp-challenges/<int:id>', methods=['GET'])
@jwt_required()
def get(id):
    return controller.get_challenge(id)
  

@cSharp.route('/c-sharp-challenges', methods=['GET'])
@jwt_required()
def get_csharp_challenges():
    return controller.get_challenges()

