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