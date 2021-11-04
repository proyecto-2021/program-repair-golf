class CSharpSrc:

	compile_code_cmd = 'mcs ' + self.path

	def __init__(self, code_file, path):
		self.code_file = code_file
		self.path = path


