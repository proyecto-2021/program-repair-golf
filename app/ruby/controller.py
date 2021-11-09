from flask import jsonify, make_response
from os import mkdir
from os.path import isdir
from tempfile import gettempdir
from shutil import rmtree
from .rubychallenge import RubyChallenge
from .rubychallengedao import RubyChallengeDAO
from .repaircandidate import RepairCandidate

class Controller:
    def __init__(self, files_path):
        self.files_path = files_path
        self.dao = RubyChallengeDAO()
        self.ruby_tmp = gettempdir() + '/ruby-tmp/'

    def post_challenge(self, code_file, tests_code_file, json):
        data = json['challenge']

        challenge = RubyChallenge(data['repair_objective'], data['complexity'])
        challenge.set_code(self.files_path, data['source_code_file_name'], code_file)
        challenge.set_code(self.files_path, data['test_suite_file_name'], tests_code_file, is_test=True)

        if not challenge.save_code():
            return make_response(jsonify({'challenge': 'source_code already exists'}), 409)

        if not challenge.save_code(is_test=True):
            challenge.remove_code()
            return make_response(jsonify({'challenge': 'test_suite already exists'}), 409)

        if not challenge.codes_compile():
            challenge.remove_code()
            challenge.remove_code(is_test=True)
            return make_response(jsonify({'challenge': 'source_code and/or test_suite doesnt compile'}), 400)

        if not challenge.dependencies_ok():
            challenge.remove_code()
            challenge.remove_code(is_test=True)
            return make_response(jsonify({'challenge': 'test_suite dependencies are wrong'}), 400)

        if not challenge.tests_fail():
            challenge.remove_code()
            challenge.remove_code(is_test=True)
            return make_response(jsonify({'challenge': 'test_suite doesnt fail'}),400)

        response = challenge.get_content()
        response['id'] = self.dao.create_challenge(**challenge.get_content_for_db())

        return jsonify({'challenge': response})

    def get_challenge(self, id):
        if not self.dao.exists(id):
                return make_response(jsonify({'challenge': 'id doesnt exist'}), 404)
        challenge = self.dao.get_challenge_data(id)
        return jsonify({'challenge': challenge})

    def get_all_challenges(self):
        challenges = self.dao.get_challenges_data()
        return jsonify({'challenges': challenges})

    def post_repair(self, id, repair_code):
        if not self.dao.exists(id):
            return make_response(jsonify({'challenge': 'id doesnt exist'}),404)
        challenge = RubyChallenge(**self.dao.get_challenge(id))
        if isdir(self.ruby_tmp):
            rmtree(self.ruby_tmp)
        mkdir(self.ruby_tmp)
        rep_candidate = RepairCandidate(challenge, repair_code, self.ruby_tmp)
        rep_candidate.save_candidate()

        if not rep_candidate.compiles():
            rmtree(self.ruby_tmp)
            return make_response(jsonify({'challenge': {'repair_code': 'is erroneous'}}),400)

        if not rep_candidate.test_ok():
            rmtree(self.ruby_tmp)
            return make_response(jsonify({'challenge': {'tests_code': 'fails'}}),200)

        new_score = rep_candidate.compute_score()

        if new_score < challenge.get_best_score() or challenge.get_best_score() == 0:
            challenge.set_best_score(new_score)
            self.dao.update_challenge(id,{'best_score':new_score})
        
        rmtree(self.ruby_tmp)
        return jsonify(rep_candidate.get_content(new_score))

    def modify_challenge(self, id, code_file, tests_code_file, json):
        if not self.dao.exists(id):
            return make_response(jsonify({'challenge': 'id doesnt exist'}), 404)

        data = {'repair_objective': None, 'complexity': None}
        data.update(json['challenge'])
        old_challenge = RubyChallenge(**self.dao.get_challenge(id))
        new_challenge = RubyChallenge(data['repair_objective'], data['complexity'])
        if isdir(self.ruby_tmp):
            rmtree(self.ruby_tmp)
        mkdir(self.ruby_tmp)
        #If files names are in the request, set new_code names to them. If not, take old_challenge name.
        nc_code_name = data['source_code_file_name'] if 'source_code_file_name' in data else old_challenge.code.get_file_name()
        nc_test_name = data['test_suite_file_name'] if 'test_suite_file_name' in data else old_challenge.tests_code.get_file_name()
        
        if code_file is not None:
            new_challenge.set_code(self.ruby_tmp, nc_code_name, code_file)
            new_challenge.save_code()
            if not new_challenge.code_compile():
                rmtree(self.ruby_tmp)
                return make_response(jsonify({'challenge': 'code doesnt compile'}), 400)
        else: #If no file is passed, set the old_challenge code as the new one (Needed to check dependencies)
            old_challenge.copy_code(self.ruby_tmp)
            new_challenge.set_code(self.ruby_tmp, old_challenge.code.get_file_name())
            new_challenge.rename_code(nc_code_name)
        
        if tests_code_file is not None:
            new_challenge.set_code(self.ruby_tmp, nc_test_name, tests_code_file, is_test=True)
            new_challenge.save_code(is_test=True)
            if not new_challenge.code_compile(is_test=True):
                rmtree(self.ruby_tmp)
                return make_response(jsonify({'challenge': 'test_suite doesnt compile'}), 400)
        else:
            old_challenge.copy_code(self.ruby_tmp, is_test=True)
            new_challenge.set_code(self.ruby_tmp, old_challenge.tests_code.get_file_name(), is_test=True)
            new_challenge.rename_code(nc_test_name, is_test=True)

        if not new_challenge.dependencies_ok():
            rmtree(self.ruby_tmp)
            return make_response(jsonify({'challenge': 'test_suite dependencies are wrong'}), 400)

        if not new_challenge.tests_fail():
            rmtree(self.ruby_tmp)
            return make_response(jsonify({'challenge': 'test_suite doesnt fail'}),400)

        # Files are ok, copy it to respective directory
        if not self.copy_files(old_challenge, new_challenge):
            return make_response(jsonify({'challenge': 'code_file_name already exists'}), 409)

        if not self.copy_files(old_challenge, new_challenge, is_test=True):
            return make_response(jsonify({'challenge': 'tests_file name already exists'}), 409)

        rmtree(self.ruby_tmp)

        #From new_challenge, take only values that must be updated.
        update_data = {key: value for (key, value) in new_challenge.get_content_for_db().items() if value is not None}
        self.dao.update_challenge(id, update_data)
        response = self.dao.get_challenge_data(id)
        return jsonify({'challenge': response})

    def copy_files(self, oc, nc, is_test=False):
        if oc.code.get_file_name() != nc.code.get_file_name():
            if not nc.move_code(self.files_path, names_match=False, is_test=is_test):
                rmtree(self.ruby_tmp)
                return False
            oc.remove_code(is_test=is_test)
        else:
            nc.move_code(self.files_path, is_test=is_test)
        return True
