from app.python.file_utils import *
from app.python.PythonSourceCode import *
from . import client
import json

# testing builder 
def test_pythonsourcecode_builder_if(client): 
    codeToRead = read_file('tests/python/example_programs_test/valid_code_1.py','rb')
    
    pythonSourceCodeInstance = PythonSourceCode(code = codeToRead ,name='matias');
    
    codeToCompare = read_file('tests/python/example_programs_test/valid_code_1.py','r')

    fileReadResult = pythonSourceCodeInstance.get_content()
    
    assert fileReadResult == codeToCompare
    assert pythonSourceCodeInstance.name == 'matias'
    assert pythonSourceCodeInstance.content == codeToRead

# testing builder 
def test_pythonsourcecode_builder_else(client): 
    path = 'tests/python/example_programs_test/valid_test_1.py'
    
    pythonSourceCodeInstance = PythonSourceCode(path=path );
    
    pathRead = read_file(path,'rb')

    assert pythonSourceCodeInstance.path == path 
    assert pythonSourceCodeInstance.name == 'valid_test_1.py'
    assert pythonSourceCodeInstance.content == pathRead

# testing builder 
def test_pythonsourcecode_builder_else_invalid(client): 
    path = 'tests/rompien2'
    
    import_error = False    
    try:
        pythonSourceCodeInstance = PythonSourceCode(path=path );
    except FileNotFoundError:
        import_error = True

    assert import_error == True 