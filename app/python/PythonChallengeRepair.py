from .PythonChallenge import PythonChallenge
from nltk import edit_distance
from .PythonSourceCode import PythonSourceCode
from .subprocess_utils import valid_python_challenge, delete_file
from .PythonChallengeDAO import PythonChallengeDAO

class PythonChallengeRepair:

    def __init__ (self, challenge, code_repair):
        self.challenge = challenge
        self.code_repair = PythonSourceCode(code = code_repair, name = self.challenge.code.name)
        
    def is_valid_repair(self): 
        return valid_python_challenge(self.code_repair.path, self.challenge.test.path,  True)
    
    def compute_repair_score(self):
        return edit_distance(self.challenge.code.content, self.code_repair.content)

    def return_content(self):
        challenge_reponse = {
                            'repair_objective': self.challenge.repair_objective, 
                            'best_score': self.challenge.best_score
                            }
        return challenge_reponse

    def delete_temp(self):
        delete_file(self.challenge.test.path)
        delete_file(self.code_repair.path)

    #Save temporary code repair and test code
    def temporary_save(self, path):
        #Save code repair
        self.code_repair.move_code(path)
    
        #Save test code 
        self.challenge.test.move_code(path)        

