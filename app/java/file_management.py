from flask.helpers import make_response
from app.java.DAO_java_challenge import DAO_java_challenge
from app.java.models_java import Challenge_java
from . import java
from app import db
from flask import Flask, request, jsonify, json
from werkzeug.utils import secure_filename
import os
import os.path
from os import remove
from os import path

ALLOWED_EXTENSIONS = {'java'}
UPLOAD_FOLDER = './public/challenges/'

class FileManagement():

    # given an id it gets the code of the file
    def get_code_file_by_id(id):
        challenge_id= DAO_java_challenge.challenges_id_java(id)
        if challenge_id is not None:
            new_id = Challenge_java.__repr__(challenge_id)
            path = 'public/challenges/' + new_id['code'] + '.java'
            return FileManagement.get_code_file_by_path(path)
        raise Exception("Id not exits")
       
    # given an path file gets the code of the file
    def get_code_file_by_path(file):
        f = open(file, mode='r', encoding='utf-8')
        resp = f.read()
        f.close()
        return resp

    # given a file name it returns a dictionary with the code and test_code fields as a string
    def show_codes(name_file):
        challenge_aux = Challenge_java.query.filter_by(code = name_file).first()
        if challenge_aux is not None:
            new_var = Challenge_java.__repr__(challenge_aux)
            path = 'public/challenges/' + new_var['code'] + '.java'
            new_var['code'] = FileManagement.get_code_file_by_path(path)
            path_test = 'public/challenges/' + new_var['tests_code'] + '.java'
            new_var['tests_code'] = FileManagement.get_code_file_by_path(path_test)
            return new_var
        raise Exception("name of file no exist")
       
    # remove the of file in directory
    def delete_path(file_rm):
        if path.exists(file_rm):
            remove(file_rm)

    def upload_file_test(file, path, dict):
        if file is None:
            raise Exception("One of the provided files has syntax errors.")
        if file.filename == '' :
            raise Exception("No name of file")
        if file and FileManagement.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name_archivo_test = dict['test_suite_file_name'] + '.java'
                file.save(os.path.join(path, name_archivo_test))
    
    def upload_file_class(file, path, dict):
        if file is None:
            raise Exception("One of the provided files has syntax errors.")
        if file.filename == '' :
            raise Exception("No name of file")
        if file and FileManagement.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name_archivo = dict['source_code_file_name'] + '.java'
                file.save(os.path.join(path, name_archivo))
                
    def upload_file_repair(file, path, dict):
        if file is None:
            raise Exception("One of the provided files has syntax errors.")
        if file.filename == '' :
            raise Exception("No name of file")
        if file and FileManagement.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                name_archivo = dict['code'] + '.java'
                file.save(os.path.join(path, name_archivo))

    def allowed_file(filename):
        return '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
