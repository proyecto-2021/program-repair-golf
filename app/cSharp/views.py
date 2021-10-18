from . import cSharp

@cSharp.route('/login')
def login():
    return { 'result': 'Ok' }

@cSharp.route('c-sharp-challenges/:id/repair', methods=['POST'])
def repair_Candidate(id):
    #to do : implement this method
    pass
