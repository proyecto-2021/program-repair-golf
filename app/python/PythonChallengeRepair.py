from .PythonChallenge import PythonChallenge

class PythonChallengeRepair 


    #def valid_repair()

    #def repair_scrore()
    
    def temporary_save(path, content)
        save_file(path, 'wb', content)
    
    def challenge_code_temporary_save(challenge, path)
        test_code = challenge.tests_code
        content_test_code = read_file(test_code,'rb')
        save_file(path, 'wb', content_test_code)

    def path_temporary(path)
        return "public/temp/" + get_filename(path)
