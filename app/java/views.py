import re
from flask.helpers import make_response

from app.java.models_java import Challenge_java
from . import java
from app import db
import os
from flask import Flask, flash, request, redirect, url_for, jsonify, json
from werkzeug.utils import secure_filename
from json import loads

UPLOAD_FOLDER = './public/challenges'
ALLOWED_EXTENSIONS = {'java'}

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
        nombre_code = aux_challenge['code']
        path='public/challenges/' + nombre_code + '.java'
        file = open (path,mode='r',encoding='utf-8')
        filemostrar=file.read()
        file.close()
        aux_challenge['code']=filemostrar
        aux_challenge.pop('tests_code',None)
        all_challenges.append(aux_challenge)
    return make_response(jsonify({"challenges":all_challenges}))
  

# Get Assignment by ID
@java.route('/java-challenges/<int:id>',methods=['GET'])
def View_Challenges(id):
    challenge=Challenge_java.query.filter_by(id=id).first()
    if (challenge is None):
        return make_response(jsonify({"challenge":"Not found prueba"}),404)   
    else: 
        return make_response(jsonify({"challenge":[Challenge_java.__repr__(challenge)]}))
      

@java.route('/java-challenges/<int:id>', methods=['PUT'])
def UpdateChallenge(id):
    challenge= Challenge_java.query.filter_by(id=id).first()
    if challenge is None:
        return make_response(jsonify({"challenge":"Not Found!"}),404)
    else:
        #Recupero los datos para actualizar
        code_file_upd = request.files['source_code_file']
        test_suite_upd = request.files['test_suite_file']
        
        challenge_json = loads(request.form.get('challenge'))
        challenge_upd= challenge_json['challenge']
        repair_objetive_upd=challenge_upd['repair_objective']
        complexity_upd=challenge_upd['complexity']

        #Controlo si se obtuvieron datos para actualizar
        if code_file_upd is not None:
            challenge.code=os.path.basename(code_file_upd)
            upload_file_1(code_file_upd)
        if test_suite_upd is not None: 
            challenge.tests_code=os.path.basename(test_suite_upd)
            upload_file_1(test_suite_upd)
        if repair_objetive_upd is not None:
            challenge.repair_objetive=repair_objetive_upd
        if complexity_upd is not None:
            challenge.complexity=complexity_upd
        
        db.session.commit()
        return jsonify({"challenge":Challenge_java.__repr__(challenge)})

#java.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@java.route('/java-challenges', methods=['POST'])
def create_challenge():
    aux = request.form['challenge']
    to_dict = json.loads(aux)
    dict_final = to_dict['challenge']
    if dict_final is not None:
        code_file_name = dict_final['source_code_file_name']
        test_suite_file_name = dict_final['test_suite_file_name']
        objective = dict_final['repair_objective']
        complex = dict_final['complexity']
        challenge = Challenge_java.query.filter_by(code=code_file_name).first()
        if challenge is None:
            # check if the post request has the file part
            file = request.files['source_code_file']
            test_suite = request.files['test_suite_file']
            upload_file(file, test_suite)
                
            new_chan = Challenge_java(code=code_file_name, tests_code=test_suite_file_name, repair_objective=objective, complexity=complex, score=0)
            db.session.add(new_chan)
            db.session.commit()
            return make_response(jsonify({"challenge": Challenge_java.__repr__(new_chan)}))
        else:
            return make_response(jsonify("Nombre de archivo existente, cargue nuevamente"), 404)
    else:
        return make_response(jsonify("No ingreso los datos de los archivos java"))


def upload_file_1(file):
    if file is None:
        return make_response(jsonify({"error_message": "One of the provided files has syntax errors."}))
    if file.filename == '' :
        return make_response(jsonify("No name of file"), 404)
    if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_file(file, test_suite):
    if file is None or test_suite is None:
        return make_response(jsonify({"error_message": "One of the provided files has syntax errors."}))
        #file = request.files['source_code_file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
    if file.filename == '' or test_suite.filename == '':
        return make_response(jsonify("No name of file"), 404)
    if file and allowed_file(file.filename):
        if test_suite and allowed_file(test_suite.filename):
            filename = secure_filename(file.filename)
            testname = secure_filename(test_suite.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            test_suite.save(os.path.join(UPLOAD_FOLDER, testname))
            #print('archivo cargado, ahora se registra datos en la db')

#@java.route('/java-challenges/<int:id>/repair', methods=['POST'])
#def repair_challenge(id):
 #   file = request.files['source_code_file']
  #  challenge = Challenge_java.query.filter_by(id = id).first()
   # if challenge is not None:
        #si file es sintacticamente correcta, entonces compara file con los test suite
        #es decir file con challenge['tests_code']
        #si pasa todos los test
        #calcula puntuacion
        #score_curr = calculo_score()
        #if score_curr < challenge.score:
         #   challenge.score = score_curr
    #        db.session.add(challenge)
     #       db.session.commit()
    #else:
     #   return make_response(jsonify("Error al seleccionar archivo"))

