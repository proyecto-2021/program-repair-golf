import os, shutil

class DirectoryManagement:
	def __init__(self, path=None):
		self.path = path

	def get_path(self):
		return self.path

	def create_dir(self):
		os.makedirs(self.get_path())

	def is_dir(self):
		return os.path.isdir(self.get_path())

	def remove_dir(self):
		shutil.rmtree(self.get_path())