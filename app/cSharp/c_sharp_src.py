import subprocess, os
from subprocess import PIPE

class CSharpSrc:

	def __init__(self, code_file, path, file_name):
		self.code_file = code_file
		self.path = path
		self.file_name = file_name

	def compiles(self):
		compile_code_cmd = 'mcs ' + self.path
		return subprocess.call(compile_code_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0
