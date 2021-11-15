from .c_sharp_src import CSharpSrc
from .c_sharp_challenge import cSharpChallenge

class cSharpRepairCandidate:

 	def __init__(self,challenge,code_file,file_name,path):
 		if isinstance(cSharpChallenge,challenge):
 			self.challenge = challenge
 			self.code = CSharpSrc(code_file,file_name,path) 
 	
 	pass

	def get_code(self):
		return self.code

	def validate(self):
		return validate(self.code)
		

	def score(self):
		challenge_script = open(self.challenge.code,"r").readlines()
		repair_script = open(self.code.path,"r").readlines()
		return nltk.edit_distance(challenge_script,repair_script)
		