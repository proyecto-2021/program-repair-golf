from . import javascript
from .update_challenge import update_challenge_js

@javascript.route('/login')
def login():
    return { 'result': 'javascript' }

@javascript.route('/javascript-challenges/<int:id>', methods=['PUT'])
def update_challenge(id):
    return update_challenge_js(id)
