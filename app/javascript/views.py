from . import javascript
from .create_challenge import create_challenge_js

@javascript.route('/login')
def login():
    return { 'result': 'javascript' }

@javascript.route('/javascript-challenges', methods=['POST'])
def create_challenge():
  return create_challenge_js()