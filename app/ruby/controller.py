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

        response = challenge.get_content(exclude=['id'])
        response['id'] = self.dao.create_challenge(**challenge.get_content(exclude=['id', 'best_score'], for_db=True))

        return jsonify({'challenge': response})

    def get_challenge(self, id):
        if not self.dao.exists(id):
                return make_response(jsonify({'challenge': 'id doesnt exist'}), 404)
        challenge = RubyChallenge(**self.dao.get_challenge(id)).get_content(exclude=['id'])
        return jsonify({'challenge': challenge})

    def get_all_challenges(self):
        all_challenges = []
        for challenge in [challenge.get_dict() for challenge in self.dao.get_challenges()]:
            challenge_content = RubyChallenge(**challenge).get_content(exclude=['tests_code'])
            all_challenges.append(challenge_content)
        return jsonify({'challenges': all_challenges})

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
        nc_code_name = data['source_code_file_name'] if 'source_code_file_name' in data else old_challenge.get_file_name()
        nc_test_name = data['test_suite_file_name'] if 'test_suite_file_name' in data else old_challenge.get_file_name(is_test=True)
        
        if not self.set_new_challenge(nc_code_name, code_file, old_challenge, new_challenge):
            return make_response(jsonify({'challenge': 'code doesnt compile'}), 400)
        
        if not self.set_new_challenge(nc_test_name, tests_code_file, old_challenge, new_challenge, is_test=True):
            return make_response(jsonify({'challenge': 'test_suite doesnt compile'}), 400)

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
        update_data = {key: value for (key, value) in new_challenge.get_content(for_db=True).items() if value is not None}
        self.dao.update_challenge(id, update_data)
        response = RubyChallenge(**self.dao.get_challenge(id)).get_content(exclude=['id'])
        return jsonify({'challenge': response})

    def copy_files(self, old_challenge, new_challenge, is_test=False):
        if old_challenge.get_file_name(is_test=is_test) != new_challenge.get_file_name(is_test=is_test):
            if not new_challenge.move_code(self.files_path, names_match=False, is_test=is_test):
                rmtree(self.ruby_tmp)
                return False
            old_challenge.remove_code(is_test=is_test)
        else:
            new_challenge.move_code(self.files_path, is_test=is_test)
        return True

    def set_new_challenge(self, name, filee, old_challenge, new_challenge, is_test=False):
        if filee is not None:
            new_challenge.set_code(self.ruby_tmp, name, filee, is_test=is_test)
            new_challenge.save_code(is_test=is_test)
            if not new_challenge.code_compile(is_test=is_test):
                rmtree(self.ruby_tmp)
                return False
        else:
            old_challenge.copy_code(self.ruby_tmp, is_test=is_test)
            new_challenge.set_code(self.ruby_tmp, old_challenge.get_file_name(is_test=is_test), is_test=is_test)
            new_challenge.rename_code(name, is_test=is_test)
        return True