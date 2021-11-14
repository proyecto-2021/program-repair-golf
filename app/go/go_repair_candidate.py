from nltk import edit_distance
from .go_src import Go_src

class GoRepairCandidate:
	def __init__(self, challenge=None, repair_candidate=None):
		self.challenge = challenge
		self.repair_candidate = repair_candidate

	def distance(self):
		return edit_distance(self.repair_candidate.get_code_content(), self.challenge.code.get_code_content())
		