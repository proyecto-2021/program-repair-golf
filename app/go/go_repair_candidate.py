from nltk import edit_distance
from .go_source_code import SourceCode

class RepairCandidate:
	def __init__(self, challenge=None, dir_path=None, file_path=None):
		self.challenge = challenge
		self.dir_path = dir_path
		self.file_path = file_path
		self.tests_code = SourceCode(path=self.dir_path)
		self.repair_code = SourceCode(path=self.file_path)

	def get_content(self, user, attemps, score):
		return {
			'challenge':{
				'repair_objective': self.challenge.get_repair_objective(),
				'best_score': self.challenge.get_best_score(),
			},
			'player': {'username': user},
			'attempts': attemps,
			'score': score
		}

	def score(self):
		return edit_distance(self.repair_code.get_content(), self.challenge.get_code_content())

	def compiles(self):
		return self.repair_code.compiles(is_code=True)

	def tests_fail(self):
		return self.tests_code.tests_fail()