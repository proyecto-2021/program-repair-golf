import pytest
from app.javascript.controllers.files_controller import *

def test_get_name_file():
    result = get_name_file("tests/javascript/public/median.js")
    assert result == "median"

def test_get_file():
    result = get_file("tests/javascript/public/median.js")
    assert result == "median.js"

def test_get_directory():
    result = get_directory("tests/javascript/public/median.js")
    assert result == PurePosixPath("tests/javascript/public")
def test_is_file_suffix_1():
    result = is_file_suffix("tests/javascript/public/median.js",".js")
    assert result == True

def test_is_file_suffix_2():
    result = is_file_suffix("tests/javascript/public/median.js",".py")
    assert result == False

def test_exist_folder():
    result = exist_folder("example-challenges/javascript-challenges")
    assert result == True

def test_to_temp_file():
    result = to_temp_file("tests/javascript/public/median.js")
    assert result == "tests/javascript/public/median_tmp.js"

def test_exist_file():
    result = exist_file("tests/javascript/public/median.js")
    assert result == True

def test_upload_file_1():
    with pytest.raises(Exception):
        upload_file("median.py","tests/javascript/public/")

def test_upload_file_2():
    with pytest.raises(Exception):
        upload_file("median.js","something_made_up/median.js")

def test_upload_file_3():
    with pytest.raises(Exception):
        upload_file("median.js","tests/javascript/public/median.js")

@pytest.mark.skip
def test_upload_file_4():
    result = upload_file("mediana.js","tests/javascript/public/public3/mediana.js")
    assert result == True

def test_open_file_1():
    result = open_file("")
    assert result == "" 

def test_open_file_2():
    result = open_file("tests/javascript/public/median.js")
    assert result != ""

def test_replace_file_1():
    with pytest.raises(Exception):
        replace_file("tests/javascript/public/median.js","median.py")

def test_replace_file_2():
    with pytest.raises(Exception):
        replace_file("tests/javascript/public/medianera.js","medianas.js")

def test_replace_file_3():
    if(exist_file("tests/javascript/public/nothing.js")):
        replace_file("tests/javascript/public/nothing.js","tests/javascript/public/mediana.js")
        assert exist_file("tests/javascript/public/mediana.js")
    elif(exist_file("tests/javascript/public/mediana.js")):
        replace_file("tests/javascript/public/mediana.js","tests/javascript/public/nothing.js")
        assert exist_file("tests/javascript/public/nothing.js")

def test_replace_file_4():
    if(exist_file("tests/javascript/public/test.js")):
        replace_file("tests/javascript/public/test.js","tests/javascript/public/public2/test.js")
        assert exist_file("tests/javascript/public/public2/test.js")
    elif(exist_file("tests/javascript/public/public2/test.js")):
        replace_file("tests/javascript/public/public2/test.js","tests/javascript/public/test.js")
        assert exist_file("tests/javascript/public/test.js")