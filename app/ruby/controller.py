from flask import jsonify, make_response
from os import mkdir
from os.path import isdir
from json import loads, JSONDecodeError
from tempfile import gettempdir
from shutil import rmtree
from .rubychallenge import RubyChallenge
from .models.rubychallengedao import RubyChallengeDAO
from .repaircandidate import RepairCandidate


class Controller:
    """Handle request from API."""
    def __init__(self, files_path):
        """Initialize controller.
        
        Parameters:
            files_path (string): set where the files are stored,
            dao (RubyChallengeDAO): provide an object to manage database items,
            ruby_tmp (string): set a temporary directory.
        """
        self.files_path = files_path
        self.dao = RubyChallengeDAO()
        self.ruby_tmp = gettempdir() + '/ruby-tmp/'

    def post_challenge(self, code_file, tests_code_file, json_challenge):
        """Create a challenge and save it in the database.
        
        Parameters:
            code_file (FileStorage): persistent code file to store,
            tests_code_file (FileStorage): persistent test suite to store,
            json_challenge (dict): data to create the challenge. It must include files names and attributes.
        
        Returns:
            response (dict): a json with error/success info and a status code.
        """
        if not (code_file and tests_code_file and json_challenge):
            return make_response(jsonify({'challenge': 'the code, tests code and json challenge are necessary'}), 400)

        try:
            json = loads(json_challenge)
        except JSONDecodeError:
            return make_response(jsonify({'challenge': 'the json is not in a valid format'}), 400)

        data = json.get('challenge')

        if not data:
            return make_response(jsonify({'challenge': 'the json has no challenge field'}), 400)

        fields = ['source_code_file_name', 'test_suite_file_name', 'complexity', 'repair_objective']
        if not all(f in data for f in fields):
            return make_response(jsonify({'challenge': 'the challenge information is incomplete'}), 400)

        challenge = RubyChallenge(data['repair_objective'], data['complexity'])
        challenge.set_code(self.files_path, data['source_code_file_name'], code_file)
        challenge.set_tests_code(self.files_path, data['test_suite_file_name'], tests_code_file)

        if not challenge.data_ok():
            return make_response(jsonify({'challenge': 'the data is incomplete or invalid'}), 400)

        if not challenge.get_code().save():
            return make_response(jsonify({'challenge': 'the source code already exists'}), 409)

        if not challenge.get_tests_code().save():
            challenge.get_code().remove()
            return make_response(jsonify({'challenge': 'the test suite already exists'}), 409)

        if not challenge.get_code().compiles() or not challenge.get_tests_code().compiles():
            challenge.get_code().remove()
            challenge.get_tests_code().remove()
            return make_response(jsonify({'challenge': 'the source code and/or test suite does not compile'}), 400)

        if not challenge.get_tests_code().dependencies_ok(challenge.get_code()):
            challenge.get_code().remove()
            challenge.get_tests_code().remove()
            return make_response(jsonify({'challenge': 'the test suite dependencies are wrong'}), 400)

        if not challenge.get_tests_code().run_fails():
            challenge.get_code().remove()
            challenge.get_tests_code().remove()
            return make_response(jsonify({'challenge': 'the challenge has no errors to repair'}), 400)

        response = challenge.get_content(exclude=['id'])
        response['id'] = self.dao.create_challenge(**challenge.get_content(exclude=['id', 'best_score'], for_db=True))

        return jsonify({'challenge': response})

    def get_challenge(self, challenge_id):
        """Get a single challenge and its info from an id.
        
        Parameters:
            challenge_id (int): id of the challenge to retrieve.

        Returns:
            response (dict): a json with error/success info and a status code.
        """
        if not self.dao.exists(challenge_id):
            return make_response(jsonify({'challenge': 'the id does not exist'}), 404)
        challenge = RubyChallenge(**self.dao.get_challenge(challenge_id)).get_content(exclude=['id'])
        return jsonify({'challenge': challenge})

    def get_all_challenges(self):
        """Retrieve all challenges in the database.

        Returns:
            response (dict): a json with error/success info and a status code.
        """
        all_challenges = []
        for challenge in self.dao.get_challenges():
            challenge_content = RubyChallenge(**challenge).get_content(exclude=['tests_code'])
            all_challenges.append(challenge_content)
        return jsonify({'challenges': all_challenges})

    def post_repair(self, challenge_id, user, repair_code):
        """Create a repair candidate for a challenge and check its validity.
        
        Parameters:
            challenge_id (int): id of the challenge to attempt a repair,
            user (User): the user trying to fix the code,
            repair_code (FileStorage): file with the candidate code.

        Returns:
            response (dict): a json with error/success info and a status code.
        """

        if not repair_code:
            return make_response(jsonify({'challenge': 'a repair candidate is necessary'}), 400)

        if not self.dao.exists(challenge_id):
            return make_response(jsonify({'challenge': 'the id does not exist'}), 404)

        challenge = RubyChallenge(**self.dao.get_challenge(challenge_id))

        if isdir(self.ruby_tmp):
            rmtree(self.ruby_tmp)
        mkdir(self.ruby_tmp)

        rep_candidate = RepairCandidate(challenge, repair_code, self.ruby_tmp)
        rep_candidate.save_candidate()

        self.dao.add_attempt(challenge_id, user.id)

        if not rep_candidate.compiles():
            rmtree(self.ruby_tmp)
            return make_response(jsonify({'challenge': 'the repair candidate has syntax errors'}), 400)

        if not rep_candidate.tests_ok():
            rmtree(self.ruby_tmp)
            return make_response(jsonify({'challenge': 'the repair candidate does not solve the problem'}), 200)

        score = rep_candidate.compute_score()
        if score < challenge.get_best_score() or challenge.get_best_score() == 0:
            challenge.set_best_score(score)
            self.dao.update_challenge(challenge_id, {'best_score': score})
        
        rmtree(self.ruby_tmp)
        return jsonify(rep_candidate.get_content(user.username, self.dao.get_attempts_count(challenge_id, user.id), score))

    def modify_challenge(self, challenge_id, code_file, tests_code_file, json_challenge):
        """Modify a challenge data in the database.
        
        Parameters:
            challenge_id (int): id of the challenge to modify,
            code_file (FileStorage): persistent code file to store replacing the original,
            tests_code_file (FileStorage): persistent test suite to store replacing the original,
            json_challenge (dict): data to modify the challenge. It may contain files names and attributes.
        
        Returns:
            response (dict): a json with error/success info and a status code.
        """
        if not self.dao.exists(challenge_id):
            return make_response(jsonify({'challenge': 'the id does not exist'}), 404)

        old_challenge = RubyChallenge(**self.dao.get_challenge(challenge_id))
        new_challenge = RubyChallenge(**self.dao.get_challenge(challenge_id))

        if json_challenge is not None:
            try:
                json = loads(json_challenge)
            except JSONDecodeError:
                return make_response(jsonify({'challenge': 'the json is not in a valid format'}), 400)
            data = json.get('challenge')
            if data is None:
                return make_response(jsonify({'challenge': 'the json has no challenge field'}), 400)
            # If files names are in the request, set new_code names to them. If not, take old_challenge name.
            nc_code_name = data['source_code_file_name'] if 'source_code_file_name' in data \
                else old_challenge.get_code().get_file_name()
            nc_test_name = data['test_suite_file_name'] if 'test_suite_file_name' in data \
                else old_challenge.get_tests_code().get_file_name()
            data.pop('source_code_file_name', None)
            data.pop('test_suite_file_name', None)
            new_challenge.update(data)
        else:
            nc_code_name = old_challenge.get_code().get_file_name()
            nc_test_name = old_challenge.get_tests_code().get_file_name()
            
        if isdir(self.ruby_tmp):
            rmtree(self.ruby_tmp)
        mkdir(self.ruby_tmp)

        if not self.set_new_code(nc_code_name, code_file, old_challenge.get_code(), new_challenge.get_code()):
            return make_response(jsonify({'challenge': 'the source code does not compile'}), 400)
        
        if not self.set_new_code(nc_test_name, tests_code_file, old_challenge.get_tests_code(), new_challenge.get_tests_code()):
            return make_response(jsonify({'challenge': 'the test suite does not compile'}), 400)

        if not new_challenge.data_ok():
            return make_response(jsonify({'challenge': 'the data is incomplete or invalid'}), 400)

        if not new_challenge.get_tests_code().dependencies_ok(new_challenge.get_code()):
            rmtree(self.ruby_tmp)
            return make_response(jsonify({'challenge': 'the test suite dependencies are wrong'}), 400)

        if not new_challenge.get_tests_code().run_fails():
            rmtree(self.ruby_tmp)
            return make_response(jsonify({'challenge': 'the challenge has no errors to repair'}), 400)

        # Files are ok, copy it to respective directory
        if not self.copy_files(old_challenge.get_code(), new_challenge.get_code()):
            return make_response(jsonify({'challenge': 'the code file name already exists'}), 409)

        if not self.copy_files(old_challenge.get_tests_code(), new_challenge.get_tests_code()):
            return make_response(jsonify({'challenge': 'the tests file name already exists'}), 409)

        rmtree(self.ruby_tmp)

        # From new_challenge, take only values that must be updated.
        update_data = new_challenge.get_content(for_db=True, exclude=['id'])
        self.dao.update_challenge(challenge_id, update_data)
        response = RubyChallenge(**self.dao.get_challenge(challenge_id)).get_content(exclude=['id'])
        return jsonify({'challenge': response})

    def copy_files(self, old_challenge_code, new_challenge_code):
        """Copies files on demand for modify_challenge.
        
        Parameters:
            old_challenge_code (RubyCode): original challenge code being replaced,
            new_challenge_code (RubyCode): new challenge code being saved.
        
        Returns:
            Bool: False if trying to replace a file related to another challenge. True if success.
        """
        if old_challenge_code.get_file_name() != new_challenge_code.get_file_name():
            if not new_challenge_code.move(self.files_path, names_match=False):
                rmtree(self.ruby_tmp)
                return False
            old_challenge_code.remove()
        else:
            new_challenge_code.move(self.files_path)
        return True

    def set_new_code(self, name, file, old_challenge_code, new_challenge_code):
        """Set new challenge code.
        
        Parameters:
            name (String): name with which the code is saved,
            file (FileStorage/String): code to be saved. If it is a FileStorage, save it.
                If it is a String, copy the file that the String references,
            old_challenge_code (RubyCode): original challenge code,
            new_challenge_code (RubyCode): new challenge code.

        Returns:
            Bool: False if the new code fails to compile. True in other cases.
        """
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
