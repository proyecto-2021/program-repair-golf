class CSharpSrc:

	compile_code_cmd = 'mcs ' + self.path

	def __init__(self, code_file, path, file_name):
		self.code_file = code_file
		self.path = path
		self.file_name = file_name
