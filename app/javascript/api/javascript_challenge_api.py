from flask.views import MethodView
import json
import sqlite3
import traceback
from .. import javascript
from ..controllers.challenge_controller import ChallengeController
from ..controllers.challenge_repair_controller import ChallengeRepairController
from ..exceptions.ChallengeRepairException import ChallengeRepairException
from ..exceptions.CommandRunException import CommandRunException
from ..exceptions.FileUploadException import FileUploadException
from ..exceptions.FileReplaceException import FileReplaceException
from ..exceptions.challenge_dao_exception import challenge_dao_exception
from flask import jsonify, make_response,request


class JavascriptChallengeAPI(MethodView):
    @jwt_required()
    def get(self, id):
        try: 
            if not id: 
                list_challenge = ChallengeController.get_challenges()    
                return make_response(jsonify({'Challenges': list_challenge}), 200) 
            else: 
                challenge = ChallengeController.get_challenge(id)
                return make_response(jsonify({'Challenge': challenge}), 200) 
        except CommandRunException as e: 
            return make_response(jsonify({'Error': e.msg }), e.HTTP_code)
        except FileUploadException as e:
            return make_response(jsonify({'Error': e.msg }), e.HTTP_code)
        except challenge_dao_exception as e:     
            return make_response(jsonify({'Error sqlite3': e.msg}), e.HTTP_code)
        except Exception as e:
            return make_response(jsonify({'Error App': str(traceback.format_exc())}), 404)

    @jwt_required()
    def post(self,id):
        try:
            if not id: 
                data_requ = request.form
                if not data_requ:
                    return make_response(jsonify({'Challenge': 'Data not found'}), 404)
                    
                challenge_json = json.loads(data_requ.get('challenge'))['challenge']
                source_code_file = request.files['source_code_file']
                test_suite_file = request.files['test_suite_file']
                
                code_file_name = challenge_json['source_code_file_name'] or get_name_file(source_code_file.file_name)  
                test_file_name = challenge_json['test_suite_file_name'] or get_name_file(test_suite_file.file_name) 
                repair_objective = challenge_json['repair_objective'] or None
                complexity = challenge_json['complexity'] or None
                challenge = ChallengeController.create_challenge(source_code_file, test_suite_file, repair_objective, complexity, code_file_name, test_file_name)
                return make_response(jsonify({'Challenge': challenge}), 200) 
            else: 
                code_files_new = request.files['source_code_file']
                #debemos pasarle current_identity
                challenge_rep = ChallengeRepairController.repair(id, code_files_new)
                #debemos guardar el intento de este usuario en la base
                return make_response(jsonify({'Challenge': challenge_rep}), 200) 
        except CommandRunException as e: 
            return make_response(jsonify({'Error': e.msg }), e.HTTP_code)
        except FileUploadException as e:
            return make_response(jsonify({'Error': e.msg }), e.HTTP_code)
        except ChallengeRepairException as e: 
            return make_response(jsonify({'Error': e.msg }), e.HTTP_code)
        except challenge_dao_exception as e:     
            return make_response(jsonify({'Error sqlite3': e.msg}), e.HTTP_code)
        except Exception as e:
            return make_response(jsonify({'Error App': str(traceback.format_exc())}), 404)
        
    @jwt_required()
    def put(self, id):
        try:
            challenge_json = json.loads(request.form.get('challenge'))['challenge']
            source_code_file_upd = request.files['source_code_file'] or None
            test_suite_file_upd = request.files['test_suite_file'] or None
            repair_objective = challenge_json['repair_objective'] or None
            complexity = challenge_json['complexity'] or None
            best_score = challenge_json['best_score'] or None
            challenge_upt = ChallengeController.update_challenge(id, source_code_file_upd, test_suite_file_upd, repair_objective, complexity, best_score)
            return make_response(jsonify({'Challenge': challenge_upt}), 200) 
        except CommandRunException as e: 
            return make_response(jsonify({'Error': e.msg }), e.HTTP_code)
        except FileUploadException as e:
            return make_response(jsonify({'Error': e.msg }), e.HTTP_code)
        except ChallengeRepairException as e: 
            return make_response(jsonify({'Error': e.msg }), e.HTTP_code)
        except challenge_dao_exception as e:     
            return make_response(jsonify({'Error sqlite3': e.msg}), e.HTTP_code)
        except Exception as e:
            return make_response(jsonify({'Error App': str(traceback.format_exc())}), 404)
       
javascript_challenge_view = JavascriptChallengeAPI.as_view('javascript_challenge_api')
javascript.add_url_rule('/javascript-challenges', defaults={'id': None}, 
view_func=javascript_challenge_view, methods=['POST',])

javascript.add_url_rule('/javascript-challenges/', defaults={'id': None}, view_func=javascript_challenge_view, methods=['GET',])
javascript.add_url_rule('/javascript-challenges/<int:id>', view_func=javascript_challenge_view, methods=['GET', 'PUT'])
javascript.add_url_rule('/javascript-challenges/<int:id>/repair', view_func=javascript_challenge_view, methods=['POST',])        