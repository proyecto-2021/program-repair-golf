from .c_sharp_src import CSharpSrc
from .c_sharp_challenge import CSharpChallenge
import nltk

class CSharpRepairCandidate:

    def __init__(self,challenge,code_file,file_name,path):
        self.challenge = challenge
        self.code = CSharpSrc(code_file,file_name,path) 
        self.code.save()
    
    def validate(self):
        if self.code.compiles():
            if self.code.test_compiles(self.challenge.test):
                if self.code.tests_pass(self.challenge.test):
                    return 0
                return 1
        return -1
        
    def score(self):
        challenge_script = open(self.challenge.code.path,"r").readlines()
        repair_script = open(self.code.path,"r").readlines()
        return nltk.edit_distance(challenge_script,repair_script)
        