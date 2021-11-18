from flask import jsonify, request, make_response, json
from .go_challenge_dao import goChallengeDAO
from .go_src import Go_src
from .go_challenge import GoChallengeC
from .go_repair_candidate import GoRepairCandidate
from .go_directory_management import GoDirectoryManagement

dao = goChallengeDAO()
class Controller():
	
    def __init__(self):
	    pass


    def get_all_challenges(self):
        challenges = dao.get_all_challenges()
        if not challenges:
            return make_response(jsonify({'challenges' : 'not found'}), 404)

        show = []

        for c in challenges:
            challenge = GoChallengeC(path_code=c.code,path_tests_code=c.tests_code,
                repair_objective=c.repair_objective,complexity=c.complexity)

            show.append(challenge.get_content_all())

        return jsonify({"challenges" : show})


    def get_challenge_by_id(self, id):
        if not dao.exists(id):
            return make_response(jsonify({'challenge' : 'not found'}), 404)

        c = dao.get_challenge_by_id(id)

        challenge = GoChallengeC(path_code=c.code,path_tests_code=c.tests_code,
            repair_objective=c.repair_objective,complexity=c.complexity)

        show = challenge.get_content_by_id_and_put()

        return jsonify({"challenge" : show})


    def post_challenge(self):
        challenge_data = json.loads(request.form.get('challenge'))['challenge']
        
        code_file = request.files["source_code_file"]
        code_path = 'public/challenges/' + challenge_data['source_code_file_name']
        code_file.save(code_path)

        test_suite_file = request.files["test_suite_file"]
        test_suite_path = 'public/challenges/' + challenge_data['test_suite_file_name']
        test_suite_file.save(test_suite_path)

        repair_obj = challenge_data['repair_objective']
        comp = challenge_data['complexity']

        new_challenge = GoChallengeC(path_code=code_path, path_tests_code=test_suite_path, repair_objective=repair_obj, complexity=comp)

        all_the_challenges = dao.get_all_challenges()
        for every_challenge in all_the_challenges:
            if every_challenge.code == new_challenge.get_code():
                return make_response(jsonify({"challenge": "repeated"}), 409)

        if new_challenge.code_compiles() == False:
            return make_response(jsonify({"code_file": "The code has syntax errors"}), 412)
        elif new_challenge.tests_compiles() == False:
            return make_response(jsonify({"test_code_file": "The test code has syntax errors"}), 412)
        elif new_challenge.tests_fail() == False:
            return make_response(jsonify({"ERROR: tests": "There must be at least one test that fails"}), 412)

        challenge_dao = dao.create_challenge(new_challenge.get_code(), new_challenge.get_tests_code(), new_challenge.get_repair_objective(), new_challenge.get_complexity())

        new_challenge_to_dicc = new_challenge.get_content_post()
        return jsonify({"challenge": new_challenge_to_dicc})


    def post_repair(self, id):
        if not dao.exists(id):
            return make_response(jsonify({'challenge' : 'challenge does not exist'}), 404)

        c = dao.get_challenge_by_id(id)
        challenge = GoChallengeC(path_code=c.code,path_tests_code=c.tests_code,
            repair_objective=c.repair_objective,complexity=c.complexity)

        repair_code = request.files['source_code_file']
        dir = GoDirectoryManagement(path='public/challenges/solution/')
        code = Go_src(path='public/challenges/solution/code.go')
        tests = Go_src(path='public/challenges/solution/code_test.go')

        dir.create_dir()
        code.create_file()
        repair_code.save(code.get_path())
        tests.move(challenge.get_tests_code())

        repair_candidate = GoRepairCandidate(challenge=challenge, dir_path=dir.get_path(), file_path=code.get_path())

        if not repair_candidate.compiles():
            dir.remove_dir()
            return make_response(jsonify({"source_code_file" : "with sintax errors"}), 409)

        if not repair_candidate.tests_fail():
            dir.remove_dir()
            return make_response(jsonify({"challenge" : "not solved"}), 409) 

        score = repair_candidate.score()

        dir.remove_dir()

        show = repair_candidate.get_content(score)
    
        return jsonify({"repair" : show})


    def update_a_go_challenge(id):

        if not dao.exists(id):
            return make_response(jsonify({'challenge' : 'not found'}), 404)

        data = json.loads(request.form.get('challenge'))['challenge']
        challenge_dao = dao.get_challenge_by_id(id)
        challenge = GoChallengeC(challenge_dao.id, challenge_dao.code, challenge_dao.tests_code, challenge_dao.repair_objective, challenge_dao.complexity)
        old_code  = Go_src(path = challenge.get_code())
        old_tests = Go_src(path = challenge.get_tests_code())

        temporary_directory = GoDirectoryManagement(path='example-challenges/go-challenges/tmp/')
        if request.files and not(temporary_directory.is_dir()):
            temporary_directory.create_dir()

        new_code = 'source_code_file' in request.files 
        if new_code:
            if not ('source_code_file_name' in data):
                return make_response(jsonify({"source_code_file_name" : "not found"}), 409)

            path_to_code = Go_src.create_file_tmp(temporary_directory, data['source_code_file_name'], request.files['source_code_file'])
            challenge.set_code(path_to_code.get_path())

            if not challenge.code_compiles():
                temporary_directory.remove_dir()
                return make_response(jsonify({"source_code_file" : "source code with sintax errors"}), 409)           

        new_test = 'test_suite_file' in request.files
        if new_test: 
            if not ('test_suite_file_name' in data):
                return make_response(jsonify({"test_suite_file_name" : "not found"}), 409)
            
            path_to_tests = Go_src.create_file_tmp(temporary_directory, data['test_suite_file_name'], request.files['test_suite_file'])
            challenge.set_tests_code(path_to_tests.get_path())    

            if not challenge.tests_compiles():
                temporary_directory.remove_dir()
                return make_response(jsonify({"test_suite_file" : "tests with sintax errors"}), 409)

        if new_code and new_test:
            if not challenge.tests_fail():
                temporary_directory.remove_dir()
                return make_response(jsonify({'error' : 'tests must fails'}), 412)  
    
        elif new_code and not new_test:
            temp_test_file = Go_src(path = temporary_directory.get_path() + 'temp_test.go')
            temp_test_file.rewrite_file(old_tests.get_path())
            challenge.set_tests_code(temp_test_file.get_path())
            
            if not challenge.tests_fail():
                temporary_directory.remove_dir()
                return make_response(jsonify({'error' : 'source code must fails tests'}), 412)
            
            challenge.set_tests_code(old_tests.get_path())
    
        elif not new_code and new_test:
            temp_code_file = Go_src(path = temporary_directory.get_path() + 'temp.go')
            temp_code_file.rewrite_file(old_code.get_path())
            challenge.set_code(temp_code_file.get_path())
            
            if not challenge.tests_fail():
                temporary_directory.remove_dir()
                return make_response(jsonify({'error' : 'tests must fails'}), 412)
            
            challenge.set_code(old_code.get_path())

        if new_code:
            old_code.rewrite_file(challenge.get_code())
            challenge.set_code(old_code.get_path()) 

        if new_test:
            old_tests.rewrite_file(challenge.get_tests_code())
            challenge.set_tests_code(old_tests.get_path())
        
        if request.files:
            temporary_directory.remove_dir()

        if 'repair_objective' in data and data['repair_objective'] != challenge.get_repair_objective():
            challenge.set_repair_objective(data['repair_objective'])

        if 'complexity' in data and data['complexity'] != challenge.get_complexity():
            challenge.set_complexity(data['complexity'])
        
        dao.update_challenge(challenge.get_id(), challenge.get_content(id=False, tests_code=False))

        return jsonify({'challenge' : challenge.get_content(id=False)})