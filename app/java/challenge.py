
from app.java.file_management import FileManagement
from app.java.DAO_java_challenge import DAO_java_challenge
import subprocess
from subprocess import STDOUT, PIPE
from flask.helpers import make_response
from flask import Flask, request, jsonify, json

UPLOAD_FOLDER = './public/challenges/'
PATHLIBRERIA = 'app/java/lib/junit-4.13.2.jar:public/challenges'
PATHEXECUTE = 'org.junit.runner.JUnitCore'
EJECUTARFILE = 'app/java/lib/hamcrest-all-1.3.jar:app/java/lib/junit-4.13.2.jar:public/challenges/'
REPAIRTEST = 'app/java/lib/hamcrest-all-1.3.jar:app/java/lib/junit-4.13.2.jar:/tmp/'
RUTALIBREPAIR = 'app/java/lib/junit-4.13.2.jar:/tmp/'

class Challenge():

    def isValid(file, test_suite, dict):
        # upload class java and compile
        code_file_name = dict['source_code_file_name']
        test_suite_file_name = dict['test_suite_file_name']
        FileManagement.upload_file_class(file, UPLOAD_FOLDER, dict)
        
        path_file_java = UPLOAD_FOLDER + code_file_name + '.java'
        if Challenge.class_java_compile(path_file_java):
            # upload test suite java and compile
            FileManagement.upload_file_test(test_suite, UPLOAD_FOLDER, dict)
            #path_test_java = UPLOAD_FOLDER + test_suite.filename
            path_test_java = UPLOAD_FOLDER + test_suite_file_name + '.java'
            # excute test suite java
            # excute_java_test return true if pass all test
            if Challenge.file_compile(path_test_java, path_file_java):
                if Challenge.execute_test(test_suite_file_name, code_file_name):
                    return False
                else:
                    DAO_java_challenge.create_challenge(dict)
                    return True
            else:
                return False
                
        else:
            return False
            

    def class_java_compile(path_file_java):
        try:
            Challenge.compile_java(path_file_java)
        except Exception:
            FileManagement.delete_path(path_file_java)
            return False
        return True
    
    # given an path file test and path file class
    # if not compile file test remove the files and return exception
    def file_compile(path_test_java, path_file_java):
        try:
            Challenge.compile_java_test(path_test_java)
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
        if Challenge.execute_java_test(name):
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


    def is_Valid(file, test_suite, dict):
        # upload class java and compile
        code_file_name = dict['source_code_file_name']
        test_suite_file_name = dict['test_suite_file_name']
        FileManagement.upload_file_class(file, UPLOAD_FOLDER, dict)
        
        path_file_java = UPLOAD_FOLDER + code_file_name + '.java'
        if Challenge.class_java_compile(path_file_java):
            # upload test suite java and compile
            FileManagement.upload_file_test(test_suite, UPLOAD_FOLDER, dict)
            #path_test_java = UPLOAD_FOLDER + test_suite.filename
            path_test_java = UPLOAD_FOLDER + test_suite_file_name + '.java'
            # excute test suite java
            # excute_java_test return true if pass all test
            if Challenge.file_compile(path_test_java, path_file_java):
                if Challenge.execute_test(test_suite_file_name, code_file_name):
                    return False
                else:
                    
                    return True
            else:
                return False
               
        else:
            return False
            
        

