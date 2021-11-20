import pytest

from app.javascript.models_js import *
from app.javascript.modules.source_code_module import *
from app.javascript.exceptions.CommandRunException import CommandRunException

def test_compile_js():
  #arrange
  rut = "tests/javascript/file_testing_folder/median.js"
  #act
  result = compile_js(rut) 

  assert not result == True
   
def test_excepcion_CommandRun():
  with pytest.raises(Exception):
   compile_js("tests/javascript/file_testing_folder/median.text")

def test_stest_fail_run():
  rut = "tests/javascript/file_testing_folder/median.test.js"
  result = stest_fail_run(rut)
  assert not result == True

def test_excepcion_stest_fail_run():
 with pytest.raises(Exception):
  stest_fail_run("tests/javascript/file_testing_folder/median.js")

def test_stests_is_from_to_code():
  
  assert stest_is_from_to_code("tests/javascript/file_testing_folder/median.test.js") == True