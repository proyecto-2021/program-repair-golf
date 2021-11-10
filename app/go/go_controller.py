from flask import jsonify, request, make_response, json
from .go_challenge_dao import goChallengeDAO

class Controller():
	goDAO = goChallengeDAO()

	def __init__(self):
		pass

	def get_challenges(self):
		challenges = goDAO.get_all_challenges()
		return jsonify({'challenges' : challenges})

	def get_challenge(self, id):
		challenge = goDAO.get_challenge_by_id(id)
		return jsonify({'challenge' : challenge})
		# Falta convertir a diccionario 