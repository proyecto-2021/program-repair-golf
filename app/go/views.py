from flask import Flask,jsonify,request,make_response
from . import go

import subprocess
import os

@go.route('/hello') 
def hello():
    return 'Hello World!'

@go.route('api/v1/go-challenges/<int:id>/repair', methods=['POST'])
def repair_challengue_go(id):
    code_solution_file = request.files['source_code_file']
    code_solution_path = 'public/challenges/code_solution.go'
    #Save the candidate solution for later delete this
    code_solution_file.save(code_solution_path)
    
    is_good_code_solution_file = subprocess.run(["go","build",code_solution_path],stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)
    os.remove(code_solution_path)
    
    if is_good_code_solution_file.returncode == 2:
        return make_response((jsonify({"code_solution_file":"with errors"}),409))
    
    return make_response((jsonify({"code_solution_file":"without errors"}),409))