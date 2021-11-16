from flask import jsonify, request, make_response, json
from .go_challenge_dao import goChallengeDAO
from .go_src import Go_src
from .go_challenge import GoChallengeC

class Controller():
	def __init__(self):
		pass

	dao = goChallengeDAO()

	def get_all_challenges():
    	challenges = dao.get_all_challenges()
    	if not challenges:
        	return make_response(jsonify({'challenges' : 'not found'}), 404)
    
    	show = []

    	for c in challenges:
        	challenge = GoChallengeC(path_code=c.code,path_tests_code=c.tests_code,
            	repair_objective=c.repair_objective,complexity=c.complexity)

        	show.append(challenge.get_content_all())

    	return jsonify({"challenges" : show})

	def get_challenge_by_id(id):
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