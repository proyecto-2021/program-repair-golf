from . import cSharp

@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('/c-sharp-challenges/<int:id>', methods = ['GET'])
def get_challenge(id):
    #TODO: implement this method
    return{ 'challenge': 'unsupported' }
