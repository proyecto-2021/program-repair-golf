import subprocess, os
from subprocess import PIPE

class CSharpSrc:

	NUNIT_PATH = "./app/cSharp/lib/NUnit.3.13.2/lib/net35/"
	NUNIT_LIB = "./app/cSharp/lib/NUnit.3.13.2/lib/net35/nunit.framework.dll"
	NUNIT_CONSOLE_RUNNER="./app/cSharp/lib/NUnit.ConsoleRunner.3.12.0/tools/nunit3-console.exe"

	def __init__(self, code_file, path, file_name):
		self.code_file = code_file
		self.path = path
		self.file_name = file_name

	def compiles(self):
		compile_code_cmd = 'mcs ' + self.path
		return subprocess.call(compile_code_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0

	def test_compiles(self, test):
		compile_code_cmd = 'mcs ' + self.path
		test_dll = test.path.replace('.cs', '.dll')
		cmd_export = 'export MONO_PATH=' + self.NUNIT_PATH
		test_compile_cmd = compile_code_cmd + ' ' + test.path + ' -target:library -r:' + self.NUNIT_LIB + ' -out:' + test_dll
		final_cmd = cmd_export + ' && ' + test_compile_cmd
		return subprocess.call(final_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0

	def tests_pass(self, test):
		test_dll = test.path.replace('.cs', '.dll')
		self.compiles()
		self.test_compiles(test)
		cmd_export = 'export MONO_PATH=' + self.NUNIT_PATH
		cmd_execute = 'mono ' + self.NUNIT_CONSOLE_RUNNER + ' ' + test_dll + ' -noresult'
		final_cmd = cmd_export + ' && ' + cmd_execute 
		return subprocess.call(final_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0

