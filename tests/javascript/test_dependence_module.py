import pytest
from app.javascript.models_js import *
from app.javascript.modules.dependences_module import *
from app.javascript.exceptions.CommandRunException import CommandRunException

diretory_tmp = "/tmp/"

def test_dependences_ok():
    extract_dependences(diretory_tmp)
    result = dependences_ok(diretory_tmp)
    remove_dependences(diretory_tmp)
    assert  result == True

def test_dependences_empty():
    result = dependences_ok('')
    assert  result == False

def test_dependences_extract():
    extract_dependences(diretory_tmp)
    result = dependences_ok(diretory_tmp)
    remove_dependences(diretory_tmp)
    assert result == True

def test_error_extract():
    result = False
    try: 
        sh_out = extract_dependences('')
    except CommandRunException as e:
        result = True
    finally: assert result == True     

def test_remove_dependence():
    extract_dependences(diretory_tmp)
    remove_dependences(diretory_tmp)
    result = dependences_ok(diretory_tmp)
    assert result == False



