from flask import Flask,jsonify,request,make_response
from . import go

@go.route('/hello') 
def hello():
    return 'Hello World!'

@go.route('api/v1/go-challenges/<int:id>/repair', methods=['POST'])
def repair_challengue_go(id):
    path_to_file = request.form.get('source_code_file')
    return jsonify(path_to_file)