import nltk
from flask import make_response,jsonify,request
from .files_controller import open_file, exist_file, to_temp_file, replace_file,upload_file
from ..modules.source_code_module import compile_js, test_run
from ..exceptions.ChallengeRepairException import ChallengeRepairException
from ..dao.challenge_dao import ChallengeDAO
from ..dao.attempt_dao import AttemptsDAO
from ...auth.userdao import get_user_by_id

class ChallengeRepairController():

    def repair(id,code_files_new,current_identity):
        challenge = ChallengeDAO.get_challenge(id)
        if not exist_file(challenge.code):
            raise ChallengeRepairException(f'The file does not exists{challenge.code}', ChallengeRepairException.HTTP_NOT_FOUND)
    
        file_path_new = to_temp_file(challenge.code)  
        upload_file(code_files_new, file_path_new)
        compile_js(file_path_new)
        test_run(challenge.tests_code)

        score = ChallengeRepairController.calculate_score(challenge.code,file_path_new)
        if not ChallengeRepairController.score_ok(score,challenge.best_score):
            raise ChallengeRepairException(f'The proposed score{score} is not less than the current score{challenge.best_score}', ChallengeRepairException.HTTP_NOT_FOUND)

        replace_file(file_path_new, challenge.code)
        ChallengeDAO.update_challenge(challenge.id,None,None,None,None,score)

        AttemptsDAO.create_attempt(challenge.id,current_identity)

        challenge_dict = challenge.to_dict()

        for k in ['id','code','complexity','tests_code']:
             del challenge_dict[k]

        return {'repair' :{
                            'challenge': challenge_dict,
                            'player': {'username': get_user_by_id(current_identity).name},
                            'attemps': AttemptsDAO.get_attempts_count(challenge.id,current_identity), 
                            'score': score
                        }}

    def score_ok(score,best_score):
        return score < best_score or best_score == 0    

    def calculate_score(code_current,file_path_new):
        return nltk.edit_distance(open_file(code_current), open_file(file_path_new))