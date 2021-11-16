from nltk import edit_distance
from .go_src import Go_src
from .go_challenge import GoChallenge
import os

class GoRepairCandidate:
	def __init__(self, challenge=None, repair_code=None):
		self.challenge = challenge
		self.repair_code = Go_src()

	def get_content_repair(self, score):
		return {
			'repair_objective': self.challenge.get_repair_objective(),
			'best_score': self.challenge.get_best_score(),
			'player': {'username': 'Moli'},
			'attemps': 1,
			'score': score
		}

	def score(self):
		return edit_distance(self.repair_code.get_content(), self.challenge.get_code_content())

	def code_compiles(self):
		return self.repair_code.code_compiles()

	def tests_fail(self):
		tests = Go_src(path=self.challenge.get_tests_code())
		return tests.tests_fail()

	def save(self):
		self.repair_code.save()
