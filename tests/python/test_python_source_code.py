from app.python.file_utils import *
from app.python.PythonSourceCode import *
from . import client
import json

# testing builder 
def test_pythonsourcecode_first_builder(client): 
    codeToRead = read_file('tests/python/example_programs_test/valid_code_1.py','rb')
    
    pythonSourceCodeInstance = PythonSourceCode(code = codeToRead ,name='matias');
    
    codeToCompare = read_file('tests/python/example_programs_test/valid_code_1.py','r')

    assert pythonSourceCodeInstance.name == 'matias'
    assert pythonSourceCodeInstance.content == codeToRead

# testing builder 
def test_pythonsourcecode_second_builder(client): 
    path = 'tests/python/example_programs_test/valid_atest_1.py'
    
    pythonSourceCodeInstance = PythonSourceCode(path=path );
    
    pathRead = read_file(path,'rb')

    assert pythonSourceCodeInstance.path == path 
    assert pythonSourceCodeInstance.name == 'valid_atest_1.py'
    assert pythonSourceCodeInstance.content == pathRead

# testing builder 
def test_pythonsourcecode_second_builder_invalid(client): 
    path = 'tests/rompien2'
    
    import_error = False    
    try:
        pythonSourceCodeInstance = PythonSourceCode(path=path );
    except FileNotFoundError:
        import_error = True

    assert import_error == True 

# testing method get_content
def test_pythonsourcecode_get_content(client): 
    codeToRead = read_file('tests/python/example_programs_test/valid_code_1.py','rb')

    pythonSourceCodeInstance = PythonSourceCode(code = codeToRead , name = 'matias');
    
    codeToCompare = read_file('tests/python/example_programs_test/valid_code_1.py','r')
    
    fileReadResult = pythonSourceCodeInstance.get_content()

    assert fileReadResult == codeToCompare

# testing method update
def test_pythonsourcecode_update(client):
    codeToRead = read_file('tests/python/example_programs_test/valid_code_1.py','rb')

    #name and content before update
    pythonSourceCodeInstance = PythonSourceCode(code = codeToRead , name = 'matias');
    
    codeToReadTwo = read_file('tests/python/example_programs_test/valid_code_3.py','rb')

    #name and content after update
    pythonSourceCodeInstance.update(content = codeToReadTwo, name = 'nachow')

    assert pythonSourceCodeInstance.name == 'nachow'
    assert pythonSourceCodeInstance.content == codeToReadTwo

# testing method move_code
def test_pythonsourcecode_move_code(client):
    path = 'tests/python/example_programs_test/valid_atest_1.py'
    
    name = 'valid_atest_1.py'

    pythonSourceCodeInstance = PythonSourceCode(path=path);

    path_two = 'public/temp'

    pythonSourceCodeInstance.move_code(path=path_two)

    assert pythonSourceCodeInstance.path == path_two+name   
    assert pythonSourceCodeInstance.name == name