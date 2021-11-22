from . import cSharp
from json import loads
from flask import request
from .c_sharp_controller import CSharpController
from flask_jwt import jwt_required, current_identity


controller = CSharpController()

@cSharp.route('/c-sharp-challenges/<int:id>', methods=['PUT'])
@jwt_required()
def put_csharp_challenges(id):
    return controller.update_challenge(id,request.files.get('source_code_file'),
                                       request.files.get('test_suite_file'),
                                       request.form.get('challenge'))

  
@cSharp.route('/c-sharp-challenges', methods=['POST'])
@jwt_required()  
def post_csharp_challenges():
    return controller.post_challenge(request.files.get('source_code_file'),
                                     request.files.get('test_suite_file'),
                                     request.form.get('challenge'))

@cSharp.route('c-sharp-challenges/<int:id>/repair', methods=['POST'])
@jwt_required()
def repair_candidate(id):
    return controller.post_repair_candidate(id,request.files.get('source_code_file'), current_identity)


@cSharp.route('/c-sharp-challenges/<int:id>', methods=['GET'])
@jwt_required()
def get(id):
    return controller.get_challenge(id)
  

@cSharp.route('/c-sharp-challenges', methods=['GET'])
@jwt_required()
def get_csharp_challenges():
    return controller.get_challenges()

