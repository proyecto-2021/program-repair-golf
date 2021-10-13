from . import java
from .. import db
from flask import request, make_response, jsonify
from .models_java import Challenge_java
from json import loads
import os

@java.route('/prueba')
def login():
    return { 'result': 'funciona' }

# GET 'http://localhost:4000/api/v1/java-challenges'
@java.route('/java-challenges',methods=['GET'])
def ViewAllChallenges():
    challenge = {"challenges":[]}
    challenge ['challenges'] = Challenge_java.query.all()
    all_challenges=[]
    for i in challenge['challenges']:
        aux_challenge = Challenge_java.__repr__(i)
        #aux_challenge.pop('tests_code',None)
        all_challenges.append(aux_challenge)
    return make_response(jsonify({"challenges":all_challenges}))

@java.route('/java-challenges/<int:id>', methods=['PUT'])
def UpdateChallenge(id):
    challenge= Challenge_java.query.filter_by(id=id).first()
    if challenge is None:
        return make_response(jsonify({"challenge":"Not Found!"}),404)
    else:
        #Recupero los datos para actualizar
        source_code_file_upd=request.form.get('source_code_file')
        test_suite_file_upd=request.form.get('test_suite_file')

        challenge_json = loads(request.form.get('challenge'))
        challenge_upd= challenge_json['challenge']
        repair_objetive_upd=challenge_upd['repair_objective']
        complexity_upd=challenge_upd['complexity']

        #Controlo si se obtuvieron datos para actualizar
        if source_code_file_upd is not None:
            challenge.code=os.path.basename(source_code_file_upd)
            #HACER UPLOAD ARCHIVO
        if test_suite_file_upd is not None: 
            challenge.tests_code=os.path.basename(test_suite_file_upd)
            #HACER UPLOAD ARCHIVO
        if repair_objetive_upd is not None:
            challenge.repair_objetive=repair_objetive_upd
        if complexity_upd is not None:
            challenge.complexity=complexity_upd
        db.session.commit()
        return jsonify({"challenge":Challenge_java.__repr__(challenge)})

        
