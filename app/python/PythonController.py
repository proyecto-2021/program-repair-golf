from .PythonChallengeDAO import PythonChallengeDAO
from .PythonChallenge import PythonChallenge
from .subprocess_utils import *

class PythonController:
  
  def get_all_challenges():
    all_challenges = PythonChallengeDAO.get_challenges()
    challenge_list = [] 
    for raw_challenge in all_challenges:
      #Get row as json
      challenge = PythonChallenge(challenge_data=raw_challenge).to_json()
      challenge['id'] = raw_challenge.id
      challenge.pop('tests_code', None)
      challenge_list.append(challenge)

    return challenge_list

