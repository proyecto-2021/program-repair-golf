from flask.scaffold import F
from app.java.file_management import FileManagement
from app.java.models_java import Challenge_java
import os
import subprocess
from subprocess import STDOUT, PIPE

UPLOAD_FOLDER = './public/challenges/'
UPLOAD_TMP = '/tmp/'
REPAIRTEST = 'app/java/lib/hamcrest-all-1.3.jar:app/java/lib/junit-4.13.2.jar:/tmp/'
RUTALIBREPAIR = 'app/java/lib/junit-4.13.2.jar:/tmp/'
PATHEXECUTE = 'org.junit.runner.JUnitCore'

class ChallengeCandidate():
    
    def isValid(file_repair, challenge):
        path_actual = UPLOAD_FOLDER + challenge['tests_code'] + '.java'
        path_destino = UPLOAD_TMP + challenge['tests_code'] + '.java'
        os.replace(path_actual, path_destino)
        FileManagement.upload_file_repair(file_repair, UPLOAD_TMP, challenge)
        path_file_repair = UPLOAD_TMP + challenge['code'] + '.java'
        if ChallengeCandidate.compile_repair(path_file_repair): 
            if ChallengeCandidate.compile_test_repair(path_destino):
                name_test = challenge['tests_code']
                if ChallengeCandidate.execute_test_repair(name_test):
                    os.replace(path_destino, path_actual)
                    return True
                else:
                    os.replace(path_destino, path_actual)
                    return False
            else:
                os.replace(path_destino, path_actual)
                return False
        else:
            return False

    def create_desafio(challenge):
        aux = Challenge_java.__repr__(challenge)
        desafio = {
            "repair_objective": aux['repair_objective'],
            "best_score": aux['best_score']
        }
        return desafio

    def compile_repair(path_file_java):
        try:
            ChallengeCandidate.compile(path_file_java)
        except Exception:
            return False
        return True
    
    def compile(java_file):
        subprocess.check_call(['javac', java_file])

    def compile_test_repair(path_test_java):
        try:
            ChallengeCandidate.compile_test(path_test_java)
        except Exception:
            return False
        return True

    def compile_test(java_file):
        subprocess.check_call(['javac', '-cp', RUTALIBREPAIR, java_file])

    def execute_test_repair(name):
        if ChallengeCandidate.execute_test(name):
            return True
        else:
            return False

    def execute_test(java_file):
        cmd=['java', '-cp', REPAIRTEST , PATHEXECUTE, java_file]
        proc=subprocess.Popen(cmd, stdout = PIPE, stderr = STDOUT)
        child = subprocess.Popen(cmd, stdin = PIPE)
        streamdata = child.communicate()[0]
        rc = child.returncode
        if rc == 0:
            return True
        else:
            return False        

