from app.java.models_java import Challenge_java
from flask import jsonify, make_response
from . import java

@java.route('/prueba')
def login():
    return { 'result': 'funciona' }

# GET 'http://localhost:4000/api/v1/java-challenges'
@java.route('/api/v1/java-challenges',methods=['GET'])
def ViewAllChallenges():
    challenge = {"challenges":[]}
    challenge ['challenges'] = Challenge_java.query.all()
    all_challenges=[]
    for i in challenge['challenges']:
        aux_challenge = Challenge_java.__repr__(i)
        #aux_challenge.pop('tests_code',None)
        all_challenges.append(aux_challenge)
    return make_response(jsonify({"challenges":all_challenges}))
    
