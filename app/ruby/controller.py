from flask import jsonify, make_response
from os import mkdir
from os.path import isdir
from json import loads
from tempfile import gettempdir
from shutil import rmtree
from .rubychallenge import RubyChallenge
from .models.rubychallengedao import RubyChallengeDAO
from .repaircandidate import RepairCandidate

class Controller:
    def __init__(self, files_path):
        self.files_path = files_path
        self.dao = RubyChallengeDAO()
        self.ruby_tmp = gettempdir() + '/ruby-tmp/'

    def post_challenge(self, code_file, tests_code_file, json_challenge):
        if not (code_file and tests_code_file and json_challenge):
            return make_response(jsonify({'challenge': 'code, tests_code and json challenge are necessary'}), 400)

        try:
            json = loads(json_challenge)
        except JSONDecodeError:
            return make_response(jsonify({'challenge': 'the json is not in a valid format'}))

        data = json.get('challenge')

        if not data:
            return make_response(jsonify({'challenge': 'the json hasnt challenge field'}), 400)

        fields = ['source_code_file_name','test_suite_file_name','complexity','repair_objective']
        if not all(f in data for f in fields):
            return make_response(jsonify({'challenge': 'the challenge information is incomplete'}), 400)

        challenge = RubyChallenge(data['repair_objective'], data['complexity'])
        challenge.set_code(self.files_path, data['source_code_file_name'], code_file)
        challenge.set_tests_code(self.files_path, data['test_suite_file_name'], tests_code_file)

        if not challenge.data_ok():
            return make_response(jsonify({'challenge': 'data is incomplete or invalid'}), 400)

        if not challenge.get_code().save():
            return make_response(jsonify({'challenge': 'source_code already exists'}), 409)

        if not challenge.get_tests_code().save():
            challenge.get_code().remove()
            return make_response(jsonify({'challenge': 'test_suite already exists'}), 409)

        if not challenge.get_code().compiles() or not challenge.get_tests_code().compiles():
            challenge.get_code().remove()
            challenge.get_tests_code().remove()
            return make_response(jsonify({'challenge': 'source_code and/or test_suite doesnt compile'}), 400)

        if not challenge.get_tests_code().dependencies_ok(challenge.get_code()):
            challenge.get_code().remove()
            challenge.get_tests_code().remove()
            return make_response(jsonify({'challenge': 'test_suite dependencies are wrong'}), 400)

        if not challenge.get_tests_code().run_fails():
            challenge.get_code().remove()
            challenge.get_tests_code().remove()
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
        if not repair_code:
            return make_response(jsonify({'challenge': 'repair_code is necessary'}), 400)

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

    def modify_challenge(self, id, code_file, tests_code_file, json_challenge):
        if not self.dao.exists(id):
            return make_response(jsonify({'challenge': 'id doesnt exist'}), 404)

        old_challenge = RubyChallenge(**self.dao.get_challenge(id))
        new_challenge = RubyChallenge(**self.dao.get_challenge(id))

        if json_challenge is not None:
            try:
                json = loads(json_challenge)
            except JSONDecodeError:
                return make_response(jsonify({'challenge': 'the json is not in a valid format'}))
            data = json.get('challenge')
            if data is None:
                return make_response(jsonify({'challenge': 'the json hasnt challenge field'}), 400)
            #If files names are in the request, set new_code names to them. If not, take old_challenge name.
            nc_code_name = data['source_code_file_name'] if 'source_code_file_name' in data else old_challenge.get_code().get_file_name()
            nc_test_name = data['test_suite_file_name'] if 'test_suite_file_name' in data else old_challenge.get_tests_code().get_file_name()
            data.pop('source_code_file_name', None)
            data.pop('test_suite_file_name', None)
            new_challenge.update(data)
        else:
            nc_code_name = old_challenge.get_code().get_file_name()
            nc_test_name = old_challenge.get_tests_code().get_file_name()

        if not new_challenge.data_ok():
            return make_response(jsonify({'challenge': 'data is incomplete or invalid'}), 400)
            
        if isdir(self.ruby_tmp):
            rmtree(self.ruby_tmp)
        mkdir(self.ruby_tmp)

        if not self.set_new_challenge(nc_code_name, code_file, old_challenge.get_code(), new_challenge.get_code()):
            return make_response(jsonify({'challenge': 'code doesnt compile'}), 400)
        
        if not self.set_new_challenge(nc_test_name, tests_code_file, old_challenge.get_tests_code(), new_challenge.get_tests_code()):
            return make_response(jsonify({'challenge': 'test_suite doesnt compile'}), 400)

        if not new_challenge.get_tests_code().dependencies_ok(new_challenge.get_code()):
            rmtree(self.ruby_tmp)
            return make_response(jsonify({'challenge': 'test_suite dependencies are wrong'}), 400)

        if not new_challenge.get_tests_code().run_fails():
            rmtree(self.ruby_tmp)
            return make_response(jsonify({'challenge': 'test_suite doesnt fail'}),400)

        # Files are ok, copy it to respective directory
        if not self.copy_files(old_challenge.get_code(), new_challenge.get_code()):
            return make_response(jsonify({'challenge': 'code_file_name already exists'}), 409)

        if not self.copy_files(old_challenge.get_tests_code(), new_challenge.get_tests_code()):
            return make_response(jsonify({'challenge': 'tests_file name already exists'}), 409)

        rmtree(self.ruby_tmp)

        #From new_challenge, take only values that must be updated.
        update_data = new_challenge.get_content(for_db=True, exclude=['id'])
        self.dao.update_challenge(id, update_data)
        response = RubyChallenge(**self.dao.get_challenge(id)).get_content(exclude=['id'])
        return jsonify({'challenge': response})

    def copy_files(self, old_challenge_code, new_challenge_code):
        if old_challenge_code.get_file_name() != new_challenge_code.get_file_name():
            if not new_challenge_code.move(self.files_path, names_match=False):
                rmtree(self.ruby_tmp)
                return False
            old_challenge_code.remove()
        else:
            new_challenge_code.move(self.files_path)
        return True

    def set_new_challenge(self, name, file, old_challenge_code, new_challenge_code):
        if file is not None:
            new_challenge_code.set_code(self.ruby_tmp, name, file)
            new_challenge_code.save()
            if not new_challenge_code.compiles():
                rmtree(self.ruby_tmp)
                return False
        else:
            old_challenge_code.copy(self.ruby_tmp)
            new_challenge_code.set_code(self.ruby_tmp, old_challenge_code.get_file_name())
            new_challenge_code.rename(name)
        return True