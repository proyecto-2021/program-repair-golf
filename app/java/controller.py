from flask.helpers import make_response
from app.java.DAO_java_challenge import DAO_java_challenge
from app.java.models_java import Challenge_java
from app.java.file_management import FileManagement
from . import java
from app import db
import os
from flask import Flask, request,jsonify, json
from json import loads
import subprocess
import os.path
from subprocess import STDOUT, PIPE

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
            nombre_code = aux_challenge['code']
            path='public/challenges/' + nombre_code + '.java'
            file = open (path,mode='r',encoding='utf-8')
            filemostrar=file.read()
            file.close()
            aux_challenge['code']=filemostrar
            aux_challenge.pop('tests_code',None)
            all_challenges.append(aux_challenge)
        return make_response(jsonify({"challenges":all_challenges}))

    def challenges_id_java(id):
        challenge=DAO_java_challenge.challenges_id_java(id)
        if challenge is None:
            return make_response(jsonify({"challenge": "Not exist this id"}))
        challengeaux=Challenge_java.__repr__(challenge)
        if (challengeaux is None):
            return make_response(jsonify({"challenge":"Not found prueba"}),404)   
        else: 
            #recupero el codigojava del challenge
            nombre_code = challengeaux['code']
            path='public/challenges/' + nombre_code + '.java'
            file = open (path,mode='r',encoding='utf-8')
            filemostrar=file.read()
            file.close()
            challengeaux['code']=filemostrar

            #recupero el codigojava del test
            nombre_test =challengeaux['tests_code']
            path='public/challenges/' + nombre_test + '.java'
            file = open (path,mode='r',encoding='utf-8')
            filemostrar=file.read()
            file.close()
            challengeaux['tests_code']=filemostrar
            return jsonify({"challenge":challengeaux})

    def challenge_upd_java(id):
        challenge= DAO_java_challenge.challenges_id_java()
        if challenge is None:
            return make_response(jsonify({"challenge":"Not Found!"}),404)
        else:
            challenge_json = loads(request.form.get('challenge'))
            challenge_upd= challenge_json['challenge']
        
            if 'repair_objective' in request.form.get('challenge'):
                repair_objective_upd=challenge_upd['repair_objective']
                challenge.repair_objective=repair_objective_upd
            
            if 'complexity' in request.form.get('challenge'):
                complexity_upd=challenge_upd['complexity']
                challenge.complexity=complexity_upd

            if 'source_code_file_name' in request.form:    
                code_file_upd_name=challenge_upd['source_code_file_name']

            if 'test_suite_file_name' in request.form:
                test_suite_upd_name=challenge_upd['test_suite_file_name']

            if 'source_code_file' in request.files:
                code_file_upd = request.files['source_code_file']
                path_file_java = UPLOAD_FOLDER + code_file_upd.filename
                if controller.class_java_compile(path_file_java):
                    challenge.code=os.path.split(code_file_upd.filename)[-1].split('.')[0]
                    print(challenge.code)
                    FileManagement.upload_file(code_file_upd, UPLOAD_FOLDER)
                else:
                    return make_response(jsonify("Class java not compile"))

            if 'test_suite_file' in request.files:
                test_suite_upd = request.files['test_suite_file']
                path_test_java = UPLOAD_FOLDER +  test_suite_upd.filename
                if controller.file_compile(path_test_java, path_file_java):
                    if controller.execute_test(code_file_upd_name, test_suite_upd_name):
                        return make_response(jsonify("La test suite debe fallar en almenos un caso de test para poder subirlo"))
                    else:
                        challenge.tests_code=os.path.split(test_suite_upd.filename)[-1].split('.')[0]
                        FileManagement.upload_file(test_suite_upd, UPLOAD_FOLDER)

            db.session.commit()
            return jsonify({"challenge":Challenge_java._repr_(challenge)})

    def add_challenge_java():
        #aux = request.form['challenge']
        to_dict = json.loads(request.form['challenge'])
        dict_final = to_dict['challenge']

        if dict_final is not None:
            code_file_name = dict_final['source_code_file_name']
            test_suite_file_name = dict_final['test_suite_file_name']
            #objective = dict_final['repair_objective']
            #complex = dict_final['complexity']
            challenge = DAO_java_challenge.get_challenge_by_code(code_file_name)

            if challenge is None:
            # check if the post request has the file part
                file = request.files['source_code_file']
                test_suite = request.files['test_suite_file']
            
            # upload class java and compile
                FileManagement.upload_file(file, UPLOAD_FOLDER)
                path_file_java = UPLOAD_FOLDER + file.filename
                if controller.class_java_compile(path_file_java):
                
                    # upload test suite java and compile
                    FileManagement.upload_file(test_suite, UPLOAD_FOLDER)
                    path_test_java = UPLOAD_FOLDER + test_suite.filename
                #file_compile(path_test_java, path_file_java)
            
                # excute test suite java
                # excute_java_test return true if pass all test
                    if controller.file_compile(path_test_java, path_file_java):
                        if controller.execute_test(test_suite_file_name, code_file_name):
                            return make_response(jsonify("La test suite debe fallar en almenos un caso de test para poder subirlo"))
                        else:
                            DAO_java_challenge.create_challenge(dict_final)
                            """new_chan = Challenge_java(code=code_file_name, tests_code=test_suite_file_name, repair_objective=objective, complexity=complex, score=0)
                            db.session.add(new_chan)
                            db.session.commit()"""
                            # show_codes return a dict with code class java and code test
                            output = FileManagement.show_codes(code_file_name)
                            return make_response(jsonify({"challenge": output}))
                    else:
                        return make_response(jsonify("Test suite not compile"))
                else:
                    return make_response(jsonify("Class java not compile"))
            else:
                return make_response(jsonify("Nombre de archivo existente, cargue nuevamente"), 404)
        else:
            return make_response(jsonify("No ingreso los datos de los archivos java"))


    ######### CLASS CHALLENGE ##########
    def class_java_compile(path_file_java):
        try:
            controller.compile_java(path_file_java)
        except Exception:
            FileManagement.delete_path(path_file_java)
            return False
        return True
    
    # given an path file test and path file class
    # if not compile file test remove the files and return exception
    def file_compile(path_test_java, path_file_java):
        try:
            controller.compile_java_test(path_test_java)
        except Exception:
            FileManagement.delete_path(path_file_java)
            FileManagement.delete_path(path_test_java)
            return False
        return True

    # if pass all test not save file and remove all files in public/challenges
    def execute_test(name, code_file_name):
        rm_java = UPLOAD_FOLDER + name + '.java'
        rm_class = UPLOAD_FOLDER + name + '.class'
        rm_java_class = UPLOAD_FOLDER + code_file_name + '.java'
        rm_java_java = UPLOAD_FOLDER + code_file_name + '.class'
        if controller.execute_java_test(name):
            # remove all files
            FileManagement.delete_path(rm_java)
            FileManagement.delete_path(rm_class)
            # remove class java
            FileManagement.delete_path(rm_java_class)
            FileManagement.delete_path(rm_java_java)
            return True
        else:
            FileManagement.delete_path(rm_class)
            FileManagement.delete_path(rm_java_java)
            return False

    ############## Service compilation ###################
    def compile_java(java_file):
        subprocess.check_call(['javac', java_file])

    def execute_java(java_file):
        cmd=['java', java_file]
        proc=subprocess.Popen(cmd, stdout = PIPE, stderr = STDOUT)
        input = subprocess.Popen(cmd, stdin = PIPE)
        print(proc.stdout.read())

    def compile_java_test(java_file):
        subprocess.check_call(['javac', '-cp', PATHLIBRERIA, java_file])
        
    # return True if pass all test alse false
    def execute_java_test(java_file):
        cmd=['java', '-cp', EJECUTARFILE , PATHEXECUTE, java_file]
        proc=subprocess.Popen(cmd, stdout = PIPE, stderr = STDOUT)
        child = subprocess.Popen(cmd, stdin = PIPE)
        streamdata = child.communicate()[0]
        rc = child.returncode
        if rc == 0:
            return True
        else:
            return False
        
        
        

