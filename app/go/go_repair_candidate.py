from nltk import edit_distance
from .go_src import Go_src
from .go_challenge import GoChallengeC
import os

class GoRepairCandidate:
	def __init__(self, challenge=None, dir_path=None, file_path=None):
		self.challenge = challenge
		self.dir_path = dir_path
		self.file_path = file_path
		self.repair_code = Go_src(path=self.file_path)

	def get_content(self, score):
		return {
			'repair_objective': self.challenge.get_repair_objective(),
			'best_score': self.challenge.get_best_score(),
			'player': {'username': 'Moli'},
			'attemps': 1,
			'score': score
		}

	def score(self):
		return edit_distance(self.repair_code.get_content(), self.challenge.get_code_content())

	def compiles(self):
		return self.repair_code.compiles(is_code=True)

	def tests_fail(self):
		tests = Go_src(path=self.dir_path)
		return tests.tests_fail()

	def save(self):
		self.repair_code.save()
