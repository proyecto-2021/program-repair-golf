from . import python

@python.route('/login')
def login():
    return { 'result': 'ok' }
