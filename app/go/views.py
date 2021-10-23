import json
from flask import Flask,jsonify,request,make_response

from app.go.models_go import GoChallenge
from . import go

import subprocess
import os
import shutil

@go.route('/hello') 
def hello():
    return 'Hello World!'

@go.route('api/v1/go-challenges/<int:id>/repair', methods=['POST'])
def repair_challengue_go(id):
    code_solution_file = request.files['source_code_file']
    code_solution_path = 'public/challenges/solution/code_solution.go'
    #Save the candidate solution for later delete this
    code_solution_file.save(code_solution_path)
    
    is_good_code_solution_file = subprocess.run(["go","build",code_solution_path],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    
    
    if is_good_code_solution_file.returncode == 2:
        return make_response((jsonify({"code_solution_file":"with errors"}),409))
    
    challengue = GoChallenge.query.filter_by(id=id).first()
    challengue_to_dict = challengue.convert_dict()
    tests_code = challengue_to_dict["tests_code"]
    
    #Falta eliminar esto
    shutil.copy (tests_code,"public/challenges/solution/code_test.go")
    
    #Falta probar bien
    the_challenge_is_solved = subprocess.run(["go","test"],cwd="public/challenges/solution",stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    #1 cuando fallan los test
    if the_challenge_is_solved.returncode == 1:
        return make_response((jsonify({"the challengue":"not solved"}),409))
    
    
    
    #print(type(challengue_to_dict))
    #os.remove(code_solution_path)
    return jsonify(the_challenge_is_solved.returncode)
    #return make_response((jsonify({"code_solution_file":"without errors"}),409))