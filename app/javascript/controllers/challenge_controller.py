from ..models_js import JavascriptChallenge
from ..folders_and_files import CODES_PATH, FILE_JS_EXTENSION
from ..exceptions.CommandRunException import CommandRunException
from .files_controller import upload_file, open_file, to_temp_file, replace_file, remove_files, exist_file
from ..modules.source_code_module import compile_js, stest_fail_run
from ..dao.challenge_dao import ChallengeDAO   

class ChallengeController():

    def get_challenge(id):
        challenge = ChallengeDAO.get_challenge(id)
        challenge_dict = challenge.to_dict()
        challenge_dict["code"] = open_file(challenge.code)
        challenge_dict["tests_code"] = open_file(challenge.tests_code)
        del challenge_dict['id']
        return challenge_dict

    def get_challenges():
        challenges = {"challenge":[]}
        challenges["challenge"] = ChallengeDAO.get_all_challenges()
        challenge_all = []
        
        for x in challenges['challenge']:
            challenge_dict = x.to_dict()
            challenge_dict['code'] = open_file(x.code)
            del challenge_dict['tests_code']
            challenge_all.append(challenge_dict)
        return challenge_all
        
    def update_challenge(id, source_code_file_upd, test_suite_file_upd, repair_objective, complexity, best_score):
        challenge = ChallengeDAO.get_challenge(id)
        if not exist_file(challenge.code) or not exist_file(challenge.tests_code):
            raise FileReplaceException(f'file does not exist', FileReplaceException.HTTP_NOT_FOUND)
            
        file_code_path_upd = to_temp_file(challenge.code)
        file_test_path_upd = to_temp_file(challenge.tests_code)
        
        try: 
            if source_code_file_upd:
                upload_file(source_code_file_upd,file_code_path_upd)
                compile_js(file_code_path_upd)    
                replace_file(file_code_path_upd, challenge.code)
            if test_suite_file_upd:     
                upload_file(test_suite_file_upd, file_test_path_upd)
                stest_fail_run(file_test_path_upd)  
                replace_file(file_test_path_upd, challenge.tests_code)
        except CommandRunException as e: 
            remove_files(file_code_path_upd,file_test_path_upd)
            raise CommandRunException(e.msg, e.HTTP_code)

        challenge_upd = ChallengeDAO.update_challenge(id, None, None, repair_objective, complexity, best_score)
        challenge_dict = challenge_upd.to_dict()
        challenge_dict["code"] = open_file(challenge.code)
        challenge_dict["tests_code"] = open_file(challenge.tests_code)
        return challenge_dict
   
    def create_challenge(source_code_file, test_suite_file, repair_objective, complexity, code_file_name, test_file_name):
        code_file_path = CODES_PATH + code_file_name + FILE_JS_EXTENSION 
        test_file_path = CODES_PATH + test_file_name + FILE_JS_EXTENSION  
        upload_file(source_code_file, code_file_path)
        upload_file(test_suite_file, test_file_path)
        
        try: 
            compile_js(code_file_path)
            stest_fail_run(test_file_path)
        except CommandRunException as e: 
            remove_files(code_file_path,test_file_path)
            raise CommandRunException(e.msg, e.HTTP_code)
        
        challenge = ChallengeDAO.save_challenge(code_file_path, test_file_path, repair_objective, complexity, 0)

        challenge_dict = challenge.to_dict()
        challenge_dict["code"] = open_file(challenge.code)
        challenge_dict["tests_code"] = open_file(challenge.tests_code)
        return challenge_dict