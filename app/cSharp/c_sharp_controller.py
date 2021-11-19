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

    def update_challenge(self, id, code, code_test, challenge_data):
        if challenge_data is not None:
            challenge_data = json.loads(challenge_data)
            challenge_data = challenge_data['challenge']

        challenge = self.DAO.get_challenge_db(id)
        if not self.DAO.exist(id):
            return make_response(jsonify({"challenge": "There is no challenge for this id"}), 404)
        files_keys = ("source_code_file", "test_suite_file")

        challenge_name = os.path.basename(challenge['code'])
        test_name = os.path.basename(challenge['tests_code'])
        challenge_dir = self.DAO.CHALLENGE_SAVE_PATH + challenge_name.replace('.cs', '/')
        old_challenge_path = challenge_dir + challenge_name
        old_test_path = challenge_dir + test_name
        new_challenge_path = self.DAO.CHALLENGE_VALIDATION_PATH + challenge_name
        new_test_path = self.DAO.CHALLENGE_VALIDATION_PATH + test_name
        new_challenge = code
        new_test = code_test

        if new_challenge is not None and new_test is not None:
            new_ch = CSharpChallenge(new_challenge,
                                     new_test,
                                     challenge_name,
                                     test_name,
                                     new_challenge_path,
                                     new_test_path)
            val_status = new_ch.validate()
            self.DAO.handle_put_files(val_status, old_challenge_path,
                                      old_test_path, new_ch.code.path,
                                      new_ch.test.path)
            if val_status != 1:
                return self.code_validation_response(val_status)
        elif new_challenge is not None:
            new_ch = CSharpChallenge(new_challenge,
                                     open(old_test_path, "rb"),
                                     challenge_name,
                                     test_name,
                                     new_challenge_path,
                                     old_test_path)
            val_status = new_ch.validate()
            self.DAO.handle_put_files(val_status, old_challenge_path, new_ch.test.path,
                                      new_ch.code.path)
            if val_status != 1:
                return self.code_validation_response(val_status)
        elif new_test is not None:
            new_ch = CSharpChallenge(open(old_challenge_path, "rb"),
                                     new_test,
                                     challenge_name,
                                     test_name,
                                     old_challenge_path,
                                     new_test_path)
            val_status = new_ch.validate()
            self.DAO.handle_put_files(val_status, new_ch.code.path, old_test_path,
                                      test_path=new_ch.test.path)
            if val_status != 1:
                return self.code_validation_response(val_status)

        if challenge_data is not None:
            if 'repair_objective' in challenge_data:
                self.DAO.update_challenge_data(id, {'repair_objective': challenge_data['repair_objective']})

            if 'complexity' in challenge_data:
                complexity = int(challenge_data['complexity'])
                if complexity < 1 or complexity > 5 :
                    return make_response(jsonify({'Complexity': 'Must be between 1 and 5'}), 409)
                else:
                    self.DAO.update_challenge_data(id, {'complexity': complexity})
        return make_response(jsonify({'challenge': self.DAO.get_challenge_db(id, show_files_content=True)}), 200)

    def code_validation_response(self,val_status):
        if val_status == -1:
            return make_response(jsonify({'Source code': 'Sintax errors'}), 409)
        elif val_status == 0:
            return make_response(jsonify({'Challenge': 'Must fail at least one test'}), 409)
        elif val_status == 2:
            return make_response(jsonify({'Test': 'Sintax errors'}), 409)

    def post_repair_candidate(self, id, repair_candidate):
        if self.DAO.exist(id):
            challenge = self.DAO.get_challenge_db(id)
            challenge_name = os.path.basename(challenge['code'])
            test_name = os.path.basename(challenge['tests_code'])
            if repair_candidate is None:
                return make_response(jsonify({'Repair candidate': 'Not found'}), 404)

            file = repair_candidate
            repair_path = self.DAO.CHALLENGE_VALIDATION_PATH + challenge_name
            challenge_to_repair = CSharpChallenge(open(challenge['code'], "rb"), open(challenge['tests_code'], "rb"),
                                                  challenge_name, test_name, challenge['code'], 
                                                  challenge['tests_code'])
            repair = CSharpRepairCandidate(challenge_to_repair, file, challenge_name, repair_path)
            validation_result = repair.validate()
            if validation_result == -1:
                self.DAO.remove(repair.code.path)
                return make_response(jsonify({'Repair candidate': 'Sintax error'}), 409)

            elif validation_result == 1:
                self.DAO.remove(repair.code.path)
                self.DAO.remove(repair.code.path.replace('.cs', '.exe'),
                           repair.challenge.test.path.replace(".cs", ".dll"))
                return make_response(jsonify({'Repair candidate': 'Tests not passed'}), 409)
            else:
                score = repair.score()

                if self.DAO.save_best_score(score, challenge['best_score'], id) == 0:
                    challenge['best_score'] = score

                challenge_data = {
                    "repair_objective": challenge['repair_objective'],
                    "best_score": challenge['best_score']
                }
                self.DAO.remove(repair.code.path)
                self.DAO.remove(repair.code.path.replace('.cs', '.exe'), repair.challenge.test.path.replace(".cs", ".dll"))
                return make_response(jsonify({'Repair': {'challenge': challenge_data, 'score': score}}), 200)
        else:
            return make_response(jsonify({"challenge": "There is no challenge for this id"}), 404)
