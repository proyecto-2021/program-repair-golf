from . import go

@go.route('/hello') 
def hello():
    return 'Hello World!'