from posixpath import basename
from .c_sharp_challenge import CSharpChallenge
from .c_sharp_repair_candidate import CSharpRepairCandidate
from .c_sharp_challenge_DAO import CSharpChallengeDAO
from json import loads
from flask import jsonify, make_response, json, request
import os

class CSharpController:

    DAO = CSharpChallengeDAO()

    def __init__(self):
        pass

    def get_challenge(self, id):
        if self.DAO.exist(id):
            return jsonify({'Challenge': self.DAO.get_challenge_db(id, show_files_content=True)})
        else:
            return make_response(jsonify({'Challenge': 'Not found'}), 404)

    def post_challenge(self, code_file, test_file, challenge_data):
        try:
            new_challenge = loads(challenge_data)['challenge']
            new_challenge['source_code_file'] = code_file
            new_challenge['test_suite_file'] = test_file
        except Exception:
            return make_response(jsonify({"challenge": "Data not found"}), 404)
        finally:
            keys_in_challenge = ('source_code_file_name',
                                 'test_suite_file_name',
                                 'complexity',
                                 'repair_objective')
            if not all(key in new_challenge for key in keys_in_challenge):
                return make_response(jsonify({"challenge": "Data not found"}), 404)

        required_keys = ('source_code_file_name', 'test_suite_file_name',
                         'source_code_file', 'test_suite_file',
                         'repair_objective', 'complexity')
        if all(new_challenge[key] is not None for key in required_keys):
            try:
                ch_dir = self.DAO.create_challenge_dir(new_challenge['source_code_file_name'])
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
                self.DAO.remove_challenge_dir(new_challenge['source_code_file_name'])
                return make_response(jsonify({'Test': 'At least one has to fail'}), 409)

            elif validate_response == 1:
                self.DAO.remove(new_code_exe_path, new_test_dll_path)
                complexity = int(new_challenge['complexity'])
                if complexity < 1 or complexity > 5:
                    self.DAO.remove_challenge_dir(new_challenge['source_code_file_name'])
                    return make_response(jsonify({'Complexity': 'Must be between 1 and 5'}), 409)
                new_data_id = self.DAO.save_to_db(new_challenge['repair_objective'],
                                             complexity,
                                             challenge.code.file_name,
                                             challenge.test.file_name)
                content = self.DAO.get_challenge_db(new_data_id, show_files_content=True)
                return make_response(jsonify({'challenge': content}))

            elif validate_response == 2:
                self.DAO.remove_challenge_dir(new_challenge['source_code_file_name'])
                return make_response(jsonify({'Test': 'Sintax errors'}), 409)

            else:
                self.DAO.remove_challenge_dir(new_challenge['source_code_file_name'])
                return make_response(jsonify({'Challenge': 'Sintax errors'}), 409)

        else:
            return make_response(jsonify({'challenge': 'Data not found'}), 404)

    def update_challenge(self, id, code, code_test, complexity, repair_objective):
        # To implement method
        pass
