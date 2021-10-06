from . import java

@java.route('/prueba')
def login():
    return { 'result': 'funciona' }