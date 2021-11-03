import json
from flask import Flask,jsonify,request,make_response
from app import db

from app.go.models_go import GoChallenge
from . import go

import subprocess
import os
import shutil
import nltk


@go.route('/hello') 
def hello():
    return 'Hello World!'

@go.route('api/v1/go-challenges/<int:id>/repair', methods=['POST'])
def repair_challengue_go(id):
    code_solution_file = request.files['source_code_file']
    subprocess.run(["mkdir","solution"],cwd="public/challenges",stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    code_solution_path = 'public/challenges/solution/code_solution.go'
    #Save the candidate solution for later delete this
    code_solution_file.save(code_solution_path)
    
    is_good_code_solution_file = subprocess.run(["go","build",code_solution_path],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    
    
    if is_good_code_solution_file.returncode == 2:
        return make_response((jsonify({"code_solution_file":"with errors"}),409))
    

    #Chequear la existencia de este id
    challengue_original = GoChallenge.query.filter_by(id=id).first()
    challengue_to_dict = challengue_original.convert_dict()
    tests_code = challengue_to_dict["tests_code"]
    
    #Falta eliminar esto
    shutil.copy (tests_code,"public/challenges/solution/code_test.go")
    
    #Falta probar bien
    the_challenge_is_solved = subprocess.run(["go","test"],cwd="public/challenges/solution",stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    #1 cuando fallan los test
    if the_challenge_is_solved.returncode == 1:
        return make_response((jsonify({"the challengue":"not solved"}),409))  
    
    #Esto va debajo del if
    challengue_original_code = challengue_to_dict["code"]
    
    f = open (challengue_original_code,'r')
    original_code = f.read()
    f.close()

    f = open (code_solution_path,'r')
    solution_code = f.read()
    f.close()

    edit_distance = nltk.edit_distance(original_code,solution_code)

    request_return = {
        "repair":{
            "challenge":{
                "repair_objective": challengue_to_dict["repair_objective"],
                "best_score": challengue_to_dict["best_score"]
            },
            "score": edit_distance
        }
    }

    subprocess.run(["rm","-r","solution"],cwd="public/challenges",stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    
    return jsonify(request_return)