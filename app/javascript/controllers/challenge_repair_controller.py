import nltk
from flask import make_response,jsonify,request
from controllers.files_controller import open_file, exist_file, to_temp_file, replace_file,upload_file
from .. import db
from ..modules.source_code_module import compile_js, test_run
from ..exceptions.ChallengeRepairException import ChallengeRepairException
from ..dao.challenge_dao import update_challenge

class ChallengeRepairController():

    def repair(self,challenge,code_files_new):
        if not exist_file(challenge.code):
            raise ChallengeRepairException(f'The file does not exists{challenge.code}', ChallengeRepairException.HTTP_NOT_FOUND)
    
        file_path_new = to_temp_file(challenge.code)  
        upload_file(code_files_new, file_path_new)
        compile_js(file_path_new)
        test_run(challenge.tests_code)

        score = self.calculate_score(challenge)
        if not self.score_ok(score,challenge.best_score):
            raise ChallengeRepairException(f'The proposed score{score} is not less than the current score{challenge.best_score}', ChallengeRepairException.HTTP_NOT_FOUND)

        replace_file(file_path_new, challenge.code)
        update_challenge(challenge.id,None,None,None,None,score)

        challenge_dict = challenge.to_dict()

        for k in ['id','code','complexity','tests_code']:
             del challenge_dict[k]

        return make_response(jsonify( {'repair' :{
                                'challenge': challenge_dict,
                                'player': {'username': 'user'},
                                'attemps': '1',
                                'score': score
                                }}, 200))

    def score_ok(score,best_score):
        return score < best_score or best_score == 0    

    def calculate_score(challenge):
        file_path_new = to_temp_file(challenge.code) 
        return nltk.edit_distance(open_file(challenge.code), open_file(file_path_new))