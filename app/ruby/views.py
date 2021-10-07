from . import ruby
#Some imports will be needed to use database

@ruby.route('/<string:name>')
def ruby_hello(name):
    return 'Hello ' + name

