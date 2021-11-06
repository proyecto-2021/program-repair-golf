import subprocess, os
from subprocess import PIPE

class CSharpSrc:

	NUNIT_PATH = "./app/cSharp/lib/NUnit.3.13.2/lib/net35/"
	NUNIT_LIB = "./app/cSharp/lib/NUnit.3.13.2/lib/net35/nunit.framework.dll"
	NUNIT_CONSOLE_RUNNER="./app/cSharp/lib/NUnit.ConsoleRunner.3.12.0/tools/nunit3-console.exe"

	def __init__(self, code_file, file_name, path=None):
		self.code_file = code_file
		self.file_name = file_name
		if path is not None:
			self.path = path

	# pre: <code_file> must be saved in <path>
	def compiles(self):
		compile_code_cmd = 'mcs ' + self.path
		return subprocess.call(compile_code_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0

	# pre: <code_file> must be saved in <path>
	def test_compiles(self, test):
		compile_code_cmd = 'mcs ' + self.path
		test_dll = test.path.replace('.cs', '.dll')
		cmd_export = 'export MONO_PATH=' + self.NUNIT_PATH
		test_compile_cmd = compile_code_cmd + ' ' + test.path + ' -target:library -r:' + self.NUNIT_LIB + ' -out:' + test_dll
		final_cmd = cmd_export + ' && ' + test_compile_cmd
		return subprocess.call(final_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0

	# pre: <code_file> must be saved in <path>
	def tests_pass(self, test):
		test_dll = test.path.replace('.cs', '.dll')
		self.compiles()
		self.test_compiles(test)
		cmd_export = 'export MONO_PATH=' + self.NUNIT_PATH
		cmd_execute = 'mono ' + self.NUNIT_CONSOLE_RUNNER + ' ' + test_dll + ' -noresult'
		final_cmd = cmd_export + ' && ' + cmd_execute 
		return subprocess.call(final_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0

	def save(self, path):
		new_path = path + self.file_name + '.cs'
		self.code_file.save(new_path)
		self.path = new_path

	def rm(self):
		if self.path is not None and path.isfile():
			os.remove(self.path)
		else:
			raise ValueError('Path has not been loaded or is not a file path.')