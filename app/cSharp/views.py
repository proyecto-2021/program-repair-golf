from . import cSharp

@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }
