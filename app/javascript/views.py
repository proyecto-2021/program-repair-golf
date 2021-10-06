from . import javascript

@javascript.route('/login')
def login():
    return { 'result': 'javascript' }

