import subprocess

class RubyCode(object):
	def __init__(self, path, file_name):
		self.path = path
		self.file_name = file_name

	def get_path(self):
		return self.path

	def file_name(self):
		return self.file_name

	def get_full_name(self):
		return self.path + self.file_name

	def get_content(self):
		with open(self.get_full_name()) as f:
			return f.read()

	def compiles(self):
		command = 'ruby -c ' + self.get_full_name()
		return subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0
