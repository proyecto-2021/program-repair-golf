from .PythonChallengeDAO import PythonChallengeDAO
from .PythonChallenge import PythonChallenge
from .PythonChallengeRepair import PythonChallengeRepair

class PythonController:
  
  def get_all_challenges():
    all_challenges = PythonChallengeDAO.get_challenges()
    challenge_list = [] 
    for raw_challenge in all_challenges:
      #Get row as json
      challenge = PythonChallenge(challenge_data=raw_challenge).to_json(best_score=True)
      challenge['id'] = raw_challenge.id
      challenge.pop('tests_code', None)
      challenge_list.append(challenge)

    return challenge_list

  def get_single_challenge(id):
    raw_challenge = PythonChallengeDAO.get_challenge(id)
    if raw_challenge is None:
      return {"Error": "Challenge not found"}

    response = PythonChallenge(challenge_data=raw_challenge).to_json(best_score=True)
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
    response['id'], response['best_score'] = challenge_id, 0
    return response

  def put_challenge(id, challenge_data, new_code, new_test):
    save_to = "public/challenges/"  #general path were code will be saved
    #retrieve challenge from db
    req_challenge = PythonChallengeDAO.get_challenge(id)
    if req_challenge is None:
      return {"Error": "Challenge not found"}
    
    #get as Challenge object
    original_challenge = challenge_update = PythonChallenge(challenge_data=req_challenge)
    #create a challenge with the requested updates
    challenge_update.update(code=new_code, test=new_test, challenge_data=challenge_data)
    
    validation_result = PythonController.perform_validation(challenge_update)
    if 'Error' in validation_result:
      return validation_result
    #update files in system
    original_challenge.delete()
    challenge_update.save_at(save_to)
    PythonChallengeDAO.update_challenge(id, challenge_update.to_json(content=False)) #updating in db
    #prepare response
    response = challenge_update.to_json(best_score=True)
    return response

  def repair_challenge(id, code_repair):
    
    if code_repair is None:
      return {"Error": "No repair provided"}
    
    req_challenge = PythonChallengeDAO.get_challenge(id)

    if req_challenge is None:
      return {"Error": "Challenge not found"}

    challenge = PythonChallenge(challenge_data= req_challenge)
    repair_challenge = PythonChallengeRepair(challenge, code_repair)

    path_temporary = "public/temp/"
    #save temporary codes
    repair_challenge.temporary_save(path_temporary)

    #validate repair
    result = repair_challenge.is_valid_repair()
    
    if 'Error' in result:
      return result

    #compute score
    score = repair_challenge.compute_repair_score()
    
    #update best score
    PythonChallengeDAO.update_best_score(id, score)

    #delete files 
    repair_challenge.delete_temp()

    return repair_challenge.return_content(score)

  #takes the challenge to a temp location and checks if it's valid
  @staticmethod
  def perform_validation(challenge):
    temp_path = "public/temp/"      #path to temp directory
    challenge.save_at(temp_path)

    validation_result = challenge.is_valid()
    challenge.delete()  #just deletes files in paths

    return validation_result
