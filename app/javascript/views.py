from . import javascript
from .list_challenges import list_challenges_js

@javascript.route('/login')
def login():
    return { 'result': 'javascript' }

@javascript.route('/javascript-challenges', methods=['GET'])
def javascipt_challenges():
    return list_challenges_js()