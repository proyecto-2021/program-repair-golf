from .rubycode import RubyCode, RubyTestCode

class RubyChallenge:
	def __init__(self, repair_objective, complexity, best_score=0, code=None, tests_code=None, id=None):
		self.repair_objective = repair_objective
		self.complexity = complexity
		self.best_score = best_score
		self.code = RubyCode()
		self.tests_code = RubyTestCode()
		self.id = id
		if code is not None:
			self.code = RubyCode(full_name=code)
		if tests_code is not None:
			self.tests_code = RubyTestCode(full_name=tests_code)

	def get_code(self):
		return self.code

	def get_tests_code(self):
		return self.tests_code

	def get_best_score(self):
		return self.best_score

	def get_content(self, exclude=[], for_db=False):
		dict = {
			'id': self.id,
			'code': self.code.get_content() if not for_db else self.code.get_full_name(),
			'tests_code': self.tests_code.get_content() if not for_db else self.tests_code.get_full_name(),
			'repair_objective': self.repair_objective,
			'complexity': self.complexity,
			'best_score': self.best_score
		}
		for key in exclude:
			del dict[key]
		return dict

	def set_code(self, files_path, file_name, file=None):
		self.code.set_code(files_path, file_name, file)

	def set_tests_code(self, files_path, file_name, file=None):
		self.tests_code.set_code(files_path, file_name, file)

	def set_best_score(self, new_score):
		self.best_score = new_score

	def update(self, data):
		for key, value in data.items():
			if value is not None:
				setattr(self, key, value)

	def data_ok(self):
		return self.repair_objective and self.complexity_ok() and self.code.file_name_ok() and self.tests_code.file_name_ok()

	def complexity_ok(self):
		return self.complexity.isdigit() and int(self.complexity) in range(1, 6)