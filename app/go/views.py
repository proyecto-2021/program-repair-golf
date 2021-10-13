

from . import go

@go.route('/hello') 
def hello():
    return 'Hello World!'

@go.route('api/v1/go-challenges/<int:id>/repair')
def repair_challengue_go(id):
    return 'test'