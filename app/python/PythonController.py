from .PythonChallengeDAO import PythonChallengeDAO
from .subprocess_utils import *

class PythonController:
  
  def get_all_challenges():
    all_challenges = PythonChallengeDAO.get_challenges()
    challenge_list = [] 
    for challenge in all_challenges:
        #Get row as a dictionary
        response = PythonChallengeModel.to_dict(challenge)
        #Get code from file
        response['code'] = read_file(response['code'], "r")
        response.pop('tests_code', None)
        challenge_list.append(response)

    return challenge_list

