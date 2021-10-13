from . import java
from app.java.models_java import Challenge_java
from flask import jsonify, make_response

@java.route('/prueba')
def login():
    return { 'result': 'funcionaok' }


# Get Assignment by ID
@java.route('/java-challenges/<int:id>',methods=['GET'])
def View_Challenges(id):
    Challenge=Challenge_java.query.filter_by(id=id).first()
    if (Challenge is None):
        return make_response(jsonify({"challenge":"Not found prueba"}),404)   
    else: 
        return make_response(jsonify({"challenge":[Challenge_java.__repr__(Challenge)]}))   
