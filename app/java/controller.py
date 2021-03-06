from flask.helpers import make_response
from app.java.DAO_java_challenge import DAO_java_challenge
from app.java.models_java import Challenge_java
from app.java.file_management import FileManagement
from app.java.challenge import Challenge
from app.auth.usermodel import User
from app.java.challenge_candidate import UPLOAD_TMP, ChallengeCandidate
from . import java
from app import db
import os
from flask import Flask, request,jsonify, json
from json import loads
import subprocess
import os.path
from subprocess import STDOUT, PIPE
import pathlib
import nltk
from flask_jwt import jwt_required, current_identity

UPLOAD_FOLDER = './public/challenges/'
PATHLIBRERIA = 'app/java/lib/junit-4.13.2.jar:public/challenges'
PATHEXECUTE = 'org.junit.runner.JUnitCore'
ALLOWED_EXTENSIONS = {'java'}
EJECUTARFILE= 'app/java/lib/hamcrest-all-1.3.jar:app/java/lib/junit-4.13.2.jar:public/challenges/'

class controller():
    
    def list_challenges_java():
        challenge = {"challenges":[]}
        challenge ['challenges'] = DAO_java_challenge.all_challenges_java()
        all_challenges=[]
        for i in challenge['challenges']:
            aux_challenge = Challenge_java.__repr__(i)
            path='public/challenges/' + aux_challenge['code'] + '.java'
            aux_challenge['code']= FileManagement.get_code_file_by_path(path)
            aux_challenge.pop('tests_code',None)
            all_challenges.append(aux_challenge)
        return all_challenges
    
    def challenges_id_java(id):
        challenge=DAO_java_challenge.challenges_id_java(id)
        if challenge is None:
            raise Exception('Error not exist it id')
        challengeaux=Challenge_java.__repr__(challenge)
        if (challengeaux is None):
            return make_response(jsonify({"challenge":"Not found prueba"}),404)   
        else: 
            nombre_code = challengeaux['code']
            path='public/challenges/' + nombre_code + '.java'
            
            filemostrar=FileManagement.get_code_file_by_path(path)     
            challengeaux['code']=filemostrar
             
            nombre_test =challengeaux['tests_code']
            path='public/challenges/' + nombre_test + '.java'
            
            filemostrar=FileManagement.get_code_file_by_path(path)  
            challengeaux['tests_code']=filemostrar
            return challengeaux
    
    def challenge_upd_java(id):
        challenge= DAO_java_challenge.challenges_id_java(id)
        if challenge is None:
            raise Exception("Challenge not found")
        else:
            challenge_json = loads(request.form.get('challenge'))
            challenge_upd= challenge_json['challenge']
            code_file_name=challenge.code
            
            if 'repair_objective' in request.form.get('challenge'):
                repair_objective_upd=challenge_upd['repair_objective']
                challenge.repair_objective=repair_objective_upd
            
            if 'complexity' in request.form.get('challenge'):
                complexity_upd=challenge_upd['complexity']
                if int(complexity_upd) <= 5:
                    challenge.complexity=complexity_upd
                else:
                    raise Exception("The complexity is greater than 5, it must be less than equal to 5")
    
            if 'source_code_file' in request.files:
                if 'test_suite_file' in request.files:
                    code_file_upd = request.files['source_code_file']
                    path_file_java = UPLOAD_FOLDER + code_file_upd.filename
                
                    test_suite_upd = request.files['test_suite_file']
                    path_test_java = UPLOAD_FOLDER +  test_suite_upd.filename
                
                    if 'source_code_file_name' in request.form.get('challenge') and 'test_suite_file_name' in request.form.get('challenge'):
                        code_file_upd_name=challenge_upd['source_code_file_name']
                        test_suite_upd_name=challenge_upd['test_suite_file_name']
                    
                        if Challenge.is_Valid(code_file_upd, test_suite_upd, challenge_upd):
                            challenge.code=code_file_upd_name
                            challenge.tests_code=test_suite_upd_name
                            code_file_name=code_file_upd_name
                        else:
                            raise Exception("Some file does not compile or pass all tests, some test must fail to load")
                    else: 
                        raise Exception("FileName not Exist")
                else:
                    raise Exception("File orCode not Exist")
            DAO_java_challenge.updatechallenge(challenge)
            return FileManagement.show_codes(code_file_name)    
            
   
    def add_challenge_java():
        to_dict = json.loads(request.form['challenge'])
        dict_final = to_dict['challenge']
        if dict_final is not None:
            code_file_name = dict_final['source_code_file_name']
            challenge = DAO_java_challenge.get_challenge_by_code(code_file_name)
            if challenge is None:
                file = request.files['source_code_file']
                test_suite = request.files['test_suite_file']
                if Challenge.is_Valid(file, test_suite, dict_final):
                    DAO_java_challenge.create_challenge(dict_final)
                    return FileManagement.show_codes(code_file_name)
                else:
                    raise Exception("Some file does not compile or pass all tests, some test must fail to load")
            else:
                raise Exception("Name of existing file")
        else:
            raise Exception("I do not enter data from java files")

    def repair_file(id):
        file_repair = request.files['source_code_file']
        challenge = DAO_java_challenge.challenges_id_java(id)
        if challenge is not None:
            curr = Challenge_java.__repr__(challenge)
            if ChallengeCandidate.isValid(file_repair, curr):
                code_class = FileManagement.get_code_file_by_id(id)
                ruta_file_tmp = UPLOAD_TMP + curr['code'] + '.java'
                code_repair = FileManagement.get_code_file_by_path(ruta_file_tmp)
                value_dist = nltk.edit_distance(code_class, code_repair)
                DAO_java_challenge.create_attempts_by_user(id, User.to_dict(current_identity)['id'])
                intentos = DAO_java_challenge.get_cant_attempts(id, User.to_dict(current_identity)['id'])
                if value_dist < curr['best_score']:
                    challenge.score = value_dist
                    DAO_java_challenge.update(challenge)
                    return {"repair": {"challenge": ChallengeCandidate.create_desafio(challenge),"player":{"username": User.to_dict(current_identity)['username']} ,"attempts": intentos, "score": value_dist}}
                else:
                    raise Exception(f'The editing distance is greater than or equal to the existing one, your score is: {value_dist}')
            else:
                raise Exception("Some file does not compile or pass all tests, some test must fail to load")
        else:
            raise Exception("Challenge not found")
                   
