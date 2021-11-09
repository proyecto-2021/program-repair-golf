from .PythonChallenge import PythonChallenge

class PythonChallengeRepair:

    def __init__ (self, challenge, code_repair)
        self.challenge = challenge
        self.code_repair = PythonSourceCode(code_repair, "code_repair")
        
    def temporary_save(path, content)
        save_file(path, 'wb', content)
    
    def save_in(challenge, path)
        #TODO : ver como guardar el test code
        
        #test_code = challenge.tests_code
        #content_test_code = read_file(test_code,'rb')
        #save_file(path, 'wb', content_test_code)

    def path_temporary(path)
        return "public/temp/" + get_filename(path)
