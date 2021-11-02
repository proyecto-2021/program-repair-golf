import os, subprocess

class RubyCode:
	def __init__(self, path=None, file_name=None, file=None, full_name=None):
		if full_name is None:
			self.path = path
			self.file_name = file_name
			self.file = file
			self.full_name = path + file_name + '.rb'
		else:
			self.path = os.path.dirname(full_name)
			self.file_name = os.path.basename(full_name).split('.')[0]
			self.file = None
			self.full_name = full_name

	def get_path(self):
		return self.path

	def get_file_name(self):
		return self.file_name

	def get_full_name(self):
		return self.path + self.file_name + '.rb'

	def save(self):
		if os.path.isfile(self.get_full_name()):
			return False
		self.file.save(dst=self.get_full_name())
		return True

	def remove(self):
		os.remove(self.get_full_name())

	def get_content(self):
		with open(self.get_full_name()) as f:
			return f.read()

	def compiles(self):
		command = 'ruby -c ' + self.get_full_name()
		return subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0
