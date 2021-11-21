from _pytest.compat import ascii_escaped
import pytest

from . import client,auth
from app.javascript.models_js import *
from app.javascript.modules.dependences_module import *
from app.javascript.exceptions.CommandRunException import CommandRunException


def test_dependeces_ok():
    result = dependences_ok("/public/challenges/test/javascript/file_testing_folder")
    assert  result == False

def test_depences_ok_Vacia():
    result = dependences_ok(' ')
    assert  result == False

def test_dependes_ok1():
    result = dependences_ok("tests/javascript/file_testing_folder/median.js")
    assert result == False

def test_error_extract():
    a = True
    result = error_extract(a)
    assert result == False

def test_error_extract1():
    a = ' '
    result = error_extract(a)
    assert result == False



