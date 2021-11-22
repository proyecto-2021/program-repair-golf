from . import client, jwt_token
from .atest_utils import *
import json


# testing of one invalid post challenge
def test_post_pythonChallenge(client, jwt_token):
    repair_objective = "make to pass"
    jwt_token = None
    response = send_post(client, jwt_token, "valid_code_3.py", "valid_atest_3.py", repair_objective, "2", default_code_content=False)
    assert response.status_code == 401

# testing a invalid get single challenge 
def test_get_single_pythonChallenge(client, jwt_token):
    #---- post one challenge to test ---#    
    repair_objectiveParam = "prueba test"
    jwt_token = None
    post_info = send_post(client, jwt_token, "valid_code_5.py", "valid_atest_5.py", repair_objectiveParam, "3")
    if post_info.status_code == 401:
        challenge_id = 10000000
        assert post_info.status_code == 401
    else:
        challenge_id = post_info.json['challenge']['id']
        
    result = client.get(api_url + '/' + str(challenge_id), headers={'Authorization': f'JWT {jwt_token}'})
    #---- end post ---#

    #data to be entered in the post test
    get_expected_response = create_expected_response(0, "valid_code_1.py", "3", 'prueba test', "valid_atest_5.py")

    #data obtained through the get ready for manipulation
    if result.status_code != 401:
        dataChallenge = result.json
        #I get each value within the dictionary
        repair_objective = dataChallenge['challenge']['repair_objective']
        code             = dataChallenge['challenge']['code'] 

    assert result.status_code == 401