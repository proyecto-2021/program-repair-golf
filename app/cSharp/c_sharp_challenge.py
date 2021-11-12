from c_sharp_src import CSharpSrc

class CSharpChallenge:

	def __init__(self, code, test, code_name, test_name):
		self.code = CSharpSrc(code, code_name)
		self.test = CSharpSrc(test, test_name)

	def validate():
		#TODO
		pass