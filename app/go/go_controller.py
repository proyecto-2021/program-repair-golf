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
