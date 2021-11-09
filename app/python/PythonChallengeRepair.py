from .PythonChallenge import PythonChallenge
from nltk import edit_distance

class PythonChallengeRepair:

    def __init__ (self, challenge, code_repair):
        self.challenge = challenge
        self.code_repair = PythonSourceCode(code = code_repair, name = self.challenge.code.name)
        
    def is_valid_repair(self): 
        return valid_python_challenge(self.challenge.test.path, self.code_repair.code.path, True)
    
    def compute_repair_score(self):
        return edit_distance(self.challenge.code.content, self.code_repair.code.content)

    #Save temporary code repair and test code
    def temporary_save(self, path):
        #Save code repair
        self.code_repair.move_code(path)
    
        #Save test code 
        self.challenge.test.move_code(path)        

