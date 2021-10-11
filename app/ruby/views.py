from . import ruby
from app import db
from .models import RubyChallenge
from flask import request

@ruby.route('/<string:name>')
def ruby_hello(name):
    return 'Hello ' + name

@ruby.route('/challenge/<int:id>/repair', methods=['POST'])
def post_repair(id):
    new_challenge = RubyChallenge(
        code='code',
        tests_code='tests_code',
        repair_objetive='repair_objetive',
        complexity='complexity',
        best_score='best_score'
    )
    #check if the posted code has not sintax errors
    #challenge = get_by_id(id)
    #challege.get_test_suite()
    #run the posted code with the test suite
    #compute the score
    #if the score < challenge.score()
    #update score
    #return
    return new_challenge.get_dict()
