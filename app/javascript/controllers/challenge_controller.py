from ..models_js import JavascriptChallenge
from ..folders_and_files import CODES_PATH, FILE_JS_EXTENSION
from ..exceptions.CommandRunException import CommandRunException
from .files_controller import upload_file, open_file, to_temp_file, replace_file, remove_files 
from ..modules.source_code_module import compile_js, test_fail_run
from ..dao.challenge_dao import ChallengeDAO   

class ChallengeController():

    def get_challenge(id):
        challenge = ChallengeDAO.get_challenge(id)
        challenge.code = open_file(challenge.code)
        challenge.tests_code = open_file(challenge.tests_code)
        challenge_dict = challenge.to_dict()
        del challenge_dict['id']
        return challenge_dict

    def get_challenges():
        challenges = {"challenge":[]}
        challenges["challenge"] = ChallengeDAO.get_all_challenges()
        challenge_all = []
        
        for x in challenges['challenge']:
            challenge_all.append(x.to_dict())
        return challenge_all
        
    def update_challenge(id, source_code_file_upd, test_suite_file_upd, repair_objective, complexity, best_score):
        challenge = ChallengeDAO.get_challenge(id)
        print(challenge.code)
        print(challenge.tests_code)
        file_code_path_upd = to_temp_file(challenge.code)
        file_test_path_upd = to_temp_file(challenge.tests_code)
        print(challenge.code)
        print(challenge.tests_code)
        try: 
            if source_code_file_upd:
                upload_file(source_code_file_upd,file_code_path_upd)
                compile_js(file_code_path_upd)    
                replace_file(file_code_path_upd, challenge.code)
            if test_suite_file_upd:     
                upload_file(test_suite_file_upd, file_test_path_upd)
                test_fail_run(file_test_path_upd)  
                replace_file(file_test_path_upd, challenge.tests_code)
        except CommandRunException as e: 
            remove_files(file_code_path_upd,file_test_path_upd)
            raise CommandRunException(e.msg, e.HTTP_code)

        ChallengeDAO.update_challenge(id, None, None, repair_objective, complexity, best_score)

        challenge.code = open_file(challenge.code)
        challenge.tests_code = open_file(challenge.tests_code)
        return challenge.to_dict()
   
    def create_challenge(source_code_file, test_suite_file, repair_objective, complexity, code_file_name, test_file_name):
        code_file_path = CODES_PATH + code_file_name + FILE_JS_EXTENSION 
        test_file_path = CODES_PATH + test_file_name + FILE_JS_EXTENSION  
        upload_file(source_code_file, code_file_path)
        upload_file(test_suite_file, test_file_path)
        
        try: 
            compile_js(code_file_path)
            test_fail_run(test_file_path)
        except CommandRunException as e: 
            remove_files(code_file_path,test_file_path)
            raise CommandRunException(e.msg, e.HTTP_code)
        
        challenge = ChallengeDAO.save_challenge(code_file_path, test_file_path, repair_objective, complexity, 0)

        challenge.code = open_file(challenge.code)
        challenge.tests_code = open_file(challenge.tests_code)
        return challenge.to_dict()