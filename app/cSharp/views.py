from . import cSharp

@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('/c-sharp-challenges', methods=['GET'])
def get_csharp_challenges():
    # [TODO]: implement this method
    return {'challenges': 'Unsupported View'}
