#from app.java import challenge
from app.java.models_java import Challenge_java
from . import java
from app import db

class DAO_java_challenge():

    def all_challenges_java():
        return Challenge_java.query.all()
    
    def challenges_id_java(id):
        return Challenge_java.query.filter_by(id=id).first()

    def get_challenge_by_code(code_file_name):
        return Challenge_java.query.filter_by(code=code_file_name).first()

    def create_challenge(dict):
        challenge = DAO_java_challenge.get_challenge_by_code(dict['source_code_file_name'])
        if challenge is None:
            new_chan = Challenge_java(code = dict['source_code_file_name'],
                tests_code = dict['test_suite_file_name'],
                repair_objective = dict['repair_objective'],
                complexity = dict['complexity'],
                score = 500)
            db.session.add(new_chan)
            db.session.commit()
        else:
           raise Exception("Name of the code exist")
    

