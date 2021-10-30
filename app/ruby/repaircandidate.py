from nltk import edit_distance

class RepairCandidate(object):
	def __init__(self, challenge, repair_code):
		self.challenge = challenge
		self.repair_code = repair_code

	def is_valid(self):
		if not self.challenge.is_valid() or not self.repair_code.compiles():
			return False
		pass

	def compute_score(self):
		if not self.is_valid():
			return 0
		return edit_distance(repair_code.get_content(),challenge.code.get_content())
