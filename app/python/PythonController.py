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

  def get_single_challenge(id):
    raw_challenge = PythonChallengeDAO.get_challenge(id)
    if raw_challenge is None:
      return {"Error": "Challenge not found"}

    response = PythonChallenge(challenge_data=raw_challenge).to_json()
    return response

  def post_challenge(challenge_data, src_code, test_src_code):
    save_to = "public/challenges/"  #general path were code will be saved

    challenge = PythonChallenge(challenge_data=challenge_data, code=src_code, test=test_src_code)
    validation_result = PythonController.perform_validation(challenge)
    if 'Error' in validation_result:
      return validation_result
    #save in public as official challenge
    challenge.save_at(save_to)
    challenge_id = PythonChallengeDAO.create_challenge(challenge) #save in db

    #create response
    response = challenge.to_json()
    response['id'] = challenge_id
    return {"Challenge" : response}

  #takes the challenge to a temp location and checks if it's valid
  @staticmethod
  def perform_validation(challenge):
    temp_path = "public/temp/"      #path to temp directory
    challenge.save_at(temp_path)

    validation_result = challenge.is_valid()

    delete_file(challenge.code_path())
    delete_file(challenge.test_path())

    return validation_result
