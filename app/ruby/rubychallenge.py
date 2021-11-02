from .rubycode import RubyCode
import subprocess, sys

class RubyChallenge:
	def __init__(self, repair_objective, complexity):
		self.code = None
		self.tests_code = None
		self.repair_objective = repair_objective
		self.complexity = complexity
		self.best_score = 0

	def set_code(self, files_path, file_name, file):
		self.code = RubyCode(files_path, file_name, file)

	def set_tests_code(self, files_path, file_name, file):
		self.tests_code = RubyCode(files_path, file_name, file)

	def save_code(self):
		return self.code.save()

	def save_tests_code(self):
		return self.tests_code.save()

	def remove_code(self):
		self.code.remove()

	def remove_tests_code(self):
		self.tests_code.remove()

	def codes_compile(self):
		return self.code.compiles() and self.tests_code.compiles()

	def dependencies_ok(self):
		command = 'grep "require_relative" ' + self.tests_code.get_full_name()
		p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
		dependence_name = (p.communicate()[0].decode(sys.stdout.encoding).strip().split("'")[1])
		return dependence_name == self.code.get_file_name()

	def tests_fail(self):
		command = 'ruby ' + self.tests_code.get_full_name()
		return subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) != 0

	def get_content_for_db(self):
		return {
			'code': self.code.get_full_name(),
			'tests_code': self.tests_code.get_full_name(),
			'repair_objective': self.repair_objective,
			'complexity': self.complexity
		}

	def get_content(self):
		return {
			'code': self.code.get_content(),
			'tests_code': self.tests_code.get_content(),
			'repair_objective': self.repair_objective,
			'complexity': self.complexity,
			'best_score': self.best_score
		}
