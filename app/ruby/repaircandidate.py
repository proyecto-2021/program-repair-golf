from nltk import edit_distance
from .rubycode import RubyCode

class RepairCandidate(object):
	def __init__(self, challenge, repair_code, path):
		self.challenge = challenge
		self.repair_code = RubyCode(path, self.challenge.code.get_file_name(), repair_code)
		self.path = path

	def save_candidate(self):
		self.repair_code.save()

	def compiles(self):
		return self.repair_code.compiles()

	def test_ok(self):
		test_suite = RubyCode(full_name=self.challenge.tests_code.copy(self.path))
		return not test_suite.run_fail()
	
	def compute_score(self):
		return edit_distance(self.repair_code.get_content(), self.challenge.code.get_content())

	def get_content(self, score):
		return {'repair' :
            {
                'challenge': self.challenge.get_content_for_repair(),
                'player': {'username': 'Agustin'},
                'attemps': '1',
                'score': score
            }
        }