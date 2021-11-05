from . import python
from .. import db
from flask import request, make_response, jsonify
from flask.views import MethodView
from .models import PythonChallengeModel
from .PythonController import PythonController
from .PythonChallenge import PythonChallenge
from json import loads
from os import path
from .file_utils import *
from .subprocess_utils import *
import nltk

class PythonViews(MethodView):

    def get(self, id): 
        if id is None:
            challenge_list = PythonController.get_all_challenges()
            return jsonify({"challenges": challenge_list})
        else:
            response = PythonController.get_single_challenge(id)
            if 'Error' in response:
                return make_response(jsonify(response), 409)

            return jsonify({"challenge": response}) 

    def post(self):
        #gather data for post
        challenge_data = loads(request.form.get('challenge'))['challenge']
        challenge_source_code = request.files.get('source_code_file').read()
        tests_source_code = request.files.get('test_suite_file').read()

        post_result = PythonController.post_challenge(challenge_data, challenge_source_code, tests_source_code)
        if 'Error' in post_result:
            return make_response(jsonify(post_result), 409)

        return jsonify({"challenge": post_result})

    def put(self, id):
        challenge_data = request.form.get('challenge')
        if challenge_data != None: challenge_data = loads(challenge_data)['challenge']
        
        new_code = request.files.get('source_code_file')
        if new_code is not None: new_code = new_code.read()

        new_test = request.files.get('test_suite_file')
        if new_test is not None: new_test = new_test.read()

        update_result = PythonController.put_challenge(id, challenge_data, new_code, new_test)
        if 'Error' in update_result:
            return make_response(jsonify(update_result), 409)

        return jsonify({"challenge" : update_result})

    def repair_challenge(id):
        #Challenge in db 
        challenge = PythonChallenge.query.filter_by(id=id).first()
        if challenge is None:
            return make_response(jsonify({"Challenge": "Not found"}), 404)

        #Repair candidate 
        code_repair = request.files.get('source_code_file')
        code_repair = code_repair.read()

        #Temporarily save test code and rapair candidate
        temp_code_path = "public/temp/" + (lambda x: x.split('/')[-1]) (challenge.code)
        save_file(temp_code_path, 'wb',code_repair)    
        test_code = challenge.tests_code
        content_test_code = read_file(test_code,'rb')
        temp_test_code_path = "public/temp/test-code.py"
        save_file(temp_test_code_path,'wb',content_test_code)

        #Check if repair candidate it is valid
        result = valid_python_challenge(temp_code_path,temp_test_code_path, True)    

        if 'Error' in result:
            return make_response(jsonify(result), 409)
        
        code_challenge = challenge.code
        code_challenge = read_file(code_challenge, 'rb')
        
        #Compute score of the repair solution 
        score = nltk.edit_distance(code_challenge, code_repair)
        
        challenge_reponse = {'repair_objective': challenge.repair_objective, 'best_score': challenge.best_score}
        
        #Player is coming in future releases 
        player = {'username': "John Doe"}

        response = {'challenge': challenge_reponse, 'player': player, 'attempts': 0, 'score': score}

        #Deletion of files at temp
        try:
            subprocess.call("rm " + temp_code_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            subprocess.call("rm " + temp_test_code_path, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        except CalledProcessError as err:
            return {"Error": "Internal Server Error"}
        
        #Update best score for the challenge
        if challenge.best_score == 0 or score < challenge.best_score:
            challenge_dict = PythonChallenge.to_dict(challenge)
            challenge_dict['best_score'] = score
            
            db.session.query(PythonChallenge).filter_by(id=id).update(dict(challenge_dict))
            db.session.commit()

        return jsonify({"repair": response})

python_view = PythonViews.as_view('python_api')
python.add_url_rule('/api/v1/python-challenges', defaults={'id': None}, view_func=python_view, methods=['GET'])
python.add_url_rule('/api/v1/python-challenges', view_func=python_view, methods=['POST'])
python.add_url_rule('/api/v1/python-challenges/<int:id>', view_func=python_view, methods=['GET', 'PUT'])
python.add_url_rule('/api/v1/python-challenges/<int:id>/repair', view_func=python_view, methods=['POST'])