from .rubycode import RubyCode, RubyTestsCode


class RubyChallenge:
	"""Provide handling of the given challenge"""
	def __init__(self, repair_objective, complexity, best_score=0, code=None, tests_code=None, id=None):
		"""Initialize challenge.

		Parameters:
			repair_objective (str): set the challenge repair objective,
			complexity (str): set the challenge complexity,
			best_score (integer): set the challenge score by default is 0,
			code (str): set the challenge file code,
			tests_code (str): set the challenge tests suite,
			id (integer): set the challenge id.
		"""
		self.repair_objective = repair_objective
		self.complexity = complexity
		self.best_score = best_score
		self.code = RubyCode() if code is None else RubyCode(full_name=code)
		self.tests_code = RubyTestsCode() if tests_code is None else RubyTestsCode(full_name=tests_code)
		self.id = id

	def get_code(self):
		"""Obtain the challenge file code.

			Returns:
				code (RubyCode): the file code wanted.
		"""
		return self.code

	def set_code(self, files_path, file_name, file=None):
		"""Set the challenge file code.

		Parameters:
			files_path (str): the new path,
			file_name (str): the new code file name,
			file (FileStorage): the new code file.

		Attributes:
			code (RubyCode): the challenge code file.
		"""
		self.code.set_code(files_path, file_name, file)

	def get_tests_code(self):
		"""Obtain the challenge tests suite.

		Returns:
			tests_suite (RubyCode): the tests suite wanted.
		"""
		return self.tests_code

	def set_tests_code(self, files_path, file_name, file=None):
		"""Set the challenge test suite.

		Parameters:
			files_path (str): the new path,
			file_name (str): the new tests suite file name,
			file (FileStorage): the new tests suite file.

		Attributes:
			tests_code (RubyTestsCode): the challenge tests suite.
		"""
		self.tests_code.set_code(files_path, file_name, file)

	def get_best_score(self):
		"""Obtain the challenge best score.

		Returns:
			best_score (int): the score wanted.
		"""
		return self.best_score

	def get_content(self, exclude=None, for_db=False):
		"""Obtain challenge information.

		Parameters:
			exclude (list): list of attributes to excluding,
			for_db (bool): condition to know how to get the challenge file code and/or tests suite.

		Returns:
			dict (dict): a dictionary with the challenge attributes wanted.
		"""
		dictionary = {
			'id': self.id,
			'code': self.code.get_content() if not for_db else self.code.get_full_name(),
			'tests_code': self.tests_code.get_content() if not for_db else self.tests_code.get_full_name(),
			'repair_objective': self.repair_objective,
			'complexity': self.complexity,
			'best_score': self.best_score
		}
		if exclude is None:
			exclude = []
		for key in exclude:
			del dictionary[key]
		return dictionary

	def set_best_score(self, new_score):
		"""Set the challenge score.

		Parameters:
			new_score (int): the new best score to update.

		Attributes:
			best_score (int): the challenge best score.
		"""
		self.best_score = new_score

	def update(self, data):
		"""Update the challenge with a dict of changes given.

		Parameters:
			data (dict): a dict with the attributes to be modified and their new content.
		"""
		for key, value in data.items():
			if key in dir(self):
				setattr(self, key, value)

	def data_ok(self):
		"""Check if challenge attributes are not empty or wrong.

		Returns:
			bool: reports that the repair objective is not empty and the complexity and file names are correct.
		"""
		return self.repair_objective and self.complexity_ok() and self.code.file_name_ok() and self.tests_code.file_name_ok()

	def complexity_ok(self):
		"""Check that the complexity is correct.

		Returns:
			bool: reports that the complexity is between 1 and 5.
		"""
		return self.complexity.isdigit() and int(self.complexity) in range(1, 6)
