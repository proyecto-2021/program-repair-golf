import subprocess, sys

class RubyChallenge:
	def __init__(self, id,code, tests_code, repair_objective, complexity, best_score):
		self.id = id
		self.code = code
		self.tests_code = tests_code
		self.repair_objective = repair_objective
		self.complexity = complexity
		self.best_score = best_score

	def tests_fail(self):
		command = 'ruby ' + self.code.get_full_name()
		return subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) != 0

	def dependencies_ok(self):
		command = 'grep "require_relative" ' + self.tests_code.get_path()
		p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		dependence_name = (p.communicate()[0].decode(sys.stdout.encoding).strip().split("'")[1])
		return dependence_name == self.code.file_name()

	def code_compiles(self):
		return self.code.compiles()

	def tests_code_compiles(self):
		return self.tests_code.compiles()

	def is_valid(self):
		return self.code_compiles() and self.tests_code_compiles() \
			   and self.tests_fail() and self.tests_fail()

	def get_content(self):
		return {
			'id': self.id,
			'code': self.code.get_content(),
			'tests_code': self.tests_code.get_content(),
			'repair_objective': self.repair_objective,
			'complexity': self.complexity,
			'best_score': self.best_score
		}
