from . import javascript
from .list_challenges import list_challenges_js
from .update_challenge import update_challenge_js
from .create_challenge import create_challenge_js
from .get_challenge import get_challenge_js

@javascript.route('/login')
def login():
    return { 'result': 'javascript' }

@javascript.route('/javascript-challenges', methods=['GET'])
def javascipt_challenges():
    return list_challenges_js()
  
@javascript.route('/javascript-challenges/<int:id>', methods=['PUT'])
def update_challenge(id):
    return update_challenge_js(id)

@javascript.route('/javascript-challenges', methods=['POST'])
def create_challenge():
  return create_challenge_js()
  
@javascript.route('/javascript-challenges/<int:id>', methods=['GET'])
def get_challenge(id):
  return get_challenge_js(id)