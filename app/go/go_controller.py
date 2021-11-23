from flask import jsonify, request, make_response, json 
from .go_challenge_dao import ChallengeDAO
from .go_challenge import Challenge
from .go_repair_candidate import RepairCandidate
from .go_directory_management import DirectoryManagement
from flask_jwt import jwt_required,current_identity
import math

TEMP_DIR  = "public/challenges/tmp/"
CHALL_DIR = "public/challenges/"
TEMP_CODE_FILE = "code.go"
TEMP_TEST_FILE = "code_test.go"

dao = ChallengeDAO()

class Controller():
    def __init__(self):
	    pass

    @jwt_required()
    def get_all_challenges(self):
        challenges = dao.get_all_challenges()
        if not challenges:
            return make_response(jsonify({'challenges' : 'not found'}), 404)

        show = []

        for c in challenges:
            challenge = Challenge(id=c.id,path_code=c.code,path_tests_code=c.tests_code,
                repair_objective=c.repair_objective,complexity=c.complexity,best_score=c.best_score)

            show.append(challenge.get_content(tests_code=False))
        
        return jsonify({"challenges" : show})

    @jwt_required()
    def get_challenge_by_id(self, id):
        if not dao.exists(id):
            return make_response(jsonify({'challenge' : 'not found'}), 404)

        c = dao.get_challenge_by_id(id)

        challenge = Challenge(path_code=c.code,path_tests_code=c.tests_code,
            repair_objective=c.repair_objective,complexity=c.complexity,best_score=c.best_score)

        show = challenge.get_content(id=False)

        return jsonify({"challenge" : show})

    @jwt_required()
    def post_challenge(self):
        challenge_data = json.loads(request.form.get('challenge'))['challenge']
        
        code_file = request.files["source_code_file"]
        code_path = CHALL_DIR + challenge_data['source_code_file_name']
        
        all_the_challenges = dao.get_all_challenges()
        for every_challenge in all_the_challenges:
            if every_challenge.code == code_path:
            	return make_response(jsonify({"challenge": "repeated"}), 409)
        
        code_file.save(code_path)
        test_suite_file = request.files["test_suite_file"]
        test_suite_path = CHALL_DIR + challenge_data['test_suite_file_name']
        test_suite_file.save(test_suite_path)

        repair_obj = challenge_data['repair_objective']
        comp = challenge_data['complexity']

        new_challenge = Challenge(path_code=code_path, path_tests_code=test_suite_path, repair_objective=repair_obj, complexity=comp)
        if not new_challenge.code_compiles():
        	return make_response(jsonify({"code_file": "The code has syntax errors"}), 412)
        #elif not new_challenge.tests_compiles():
        #	return make_response(jsonify({"test_code_file": "The test code has syntax errors"}), 412)
        elif not new_challenge.tests_fail():
        	return make_response(jsonify({"ERROR: tests": "There must be at least one test that fails"}), 412)

        id = dao.create_challenge(new_challenge.get_code(), new_challenge.get_tests_code(), new_challenge.get_repair_objective(), new_challenge.get_complexity())

        new_challenge.set_id(id)
        new_challenge.set_best_score(math.inf)
        new_challenge_to_dicc = new_challenge.get_content()
        return jsonify({"challenge": new_challenge_to_dicc})

    @jwt_required()
    def post_repair(self, id):
        if not dao.exists(id):
            return make_response(jsonify({'challenge' : 'challenge does not exist'}), 404)

        c = dao.get_challenge_by_id(id)
        challenge = Challenge(id=c.id, path_code=c.code,path_tests_code=c.tests_code,
            repair_objective=c.repair_objective,complexity=c.complexity,best_score=c.best_score)

        repair_code = request.files['source_code_file']
        dir = DirectoryManagement(path=TEMP_DIR)
        repair = Challenge(path_code= dir.get_path() + TEMP_CODE_FILE , path_tests_code= dir.get_path() + TEMP_TEST_FILE)

        if not (dir.is_dir()):
            dir.create_dir()
        repair.code.create_file()
        repair_code.save(repair.code.get_path())
        repair.tests_code.move(challenge.get_tests_code())

        repair_candidate = RepairCandidate(challenge=challenge, dir_path=dir.get_path(), file_path=repair.code.get_path())

        dao.add_attempt(challenge.get_id(), current_identity.id)

        if not repair_candidate.compiles():
            dir.remove_dir()
            return make_response(jsonify({"source_code_file" : "with sintax errors"}), 409)

        if repair_candidate.tests_fail():
            dir.remove_dir()
            return make_response(jsonify({"challenge" : "not solved"}), 409) 

        score = repair_candidate.score()

        dir.remove_dir()

        if score < challenge.get_best_score():
            challenge.set_best_score(score)
            dao.update_challenge(challenge.get_id(), challenge.get_content(id=False, tests_code=False))
        
        show = repair_candidate.get_content(current_identity.username, dao.get_attempts_number(challenge.get_id(), current_identity.id), score)

        return jsonify({"repair" : show})

    @jwt_required()
    def update_a_go_challenge(self, id):

        if not dao.exists(id):
            return make_response(jsonify({'challenge' : 'not found'}), 404)

        data = json.loads(request.form.get('challenge'))['challenge']
        challenge_dao = dao.get_challenge_by_id(id)
        challenge = Challenge(challenge_dao.id, challenge_dao.code, challenge_dao.tests_code, challenge_dao.repair_objective, challenge_dao.complexity)
        old_code  = challenge.get_code()
        old_tests = challenge.get_tests_code()

        temporary_directory = DirectoryManagement(path = TEMP_DIR)
        if request.files and not(temporary_directory.is_dir()):
            temporary_directory.create_dir()

        new_code = 'source_code_file' in request.files 
        if new_code:
            if not ('source_code_file_name' in data):
                return make_response(jsonify({"source_code_file_name" : "not found"}), 409)

            path_to_code = create_file_tmp(temporary_directory.get_path(), data['source_code_file_name'], request.files['source_code_file'])
            challenge.set_code(path_to_code)

            if not challenge.code_compiles():
                temporary_directory.remove_dir()
                return make_response(jsonify({"source_code_file" : "source code with sintax errors"}), 409)           

        new_test = 'test_suite_file' in request.files
        if new_test: 
            if not ('test_suite_file_name' in data):
                return make_response(jsonify({"test_suite_file_name" : "not found"}), 409)
            
            path_to_tests = create_file_tmp(temporary_directory.get_path(), data['test_suite_file_name'], request.files['test_suite_file'])
            challenge.set_tests_code(path_to_tests)    

            if not new_code and new_test:
                temp_code_file = temporary_directory.get_path() + TEMP_CODE_FILE
                challenge.rewrite_code(temp_code_file)
                challenge.set_code(temp_code_file)

                if not challenge.tests_fail():
                    temporary_directory.remove_dir()
                    return make_response(jsonify({'error' : 'tests must fails'}), 412)
                
                challenge.set_code(old_code)

            if not challenge.tests_compiles():
                temporary_directory.remove_dir()
                return make_response(jsonify({"test_suite_file" : "tests with sintax errors"}), 409)
            
        if new_code and new_test:
            if not challenge.tests_fail():
                temporary_directory.remove_dir()
                return make_response(jsonify({'error' : 'tests must fails'}), 412)  
    
        elif new_code and not new_test:
            temp_test_file = temporary_directory.get_path() + TEMP_TEST_FILE
            challenge.rewrite_tests_code(temp_test_file)
            challenge.set_tests_code(temp_test_file)
            
            if not challenge.tests_fail():
                temporary_directory.remove_dir()
                return make_response(jsonify({'error' : 'source code must fails tests'}), 412)
            
            challenge.set_tests_code(old_tests)

        if new_code:
            challenge.rewrite_code(old_code)
            challenge.set_code(old_code) 

        if new_test:
            challenge.rewrite_tests_code(old_tests)
            challenge.set_tests_code(old_tests)
        
        if request.files:
            temporary_directory.remove_dir()

        if 'repair_objective' in data and data['repair_objective'] != challenge.get_repair_objective():
            challenge.set_repair_objective(data['repair_objective'])

        if 'complexity' in data and data['complexity'] != challenge.get_complexity():
            challenge.set_complexity(data['complexity'])

        challenge.set_best_score(0)
        
        dao.update_challenge(challenge.get_id(), challenge.get_content(id=False, tests_code=False))

        return jsonify({'challenge' : challenge.get_content(id=False)})

def create_file_tmp(path, name, file):
    path_to_file = path + name
    file.save(path_to_file)
    return path_to_file