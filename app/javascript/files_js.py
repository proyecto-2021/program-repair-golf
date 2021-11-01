import os
import subprocess
from pathlib import PurePath, PurePosixPath
import json
from ..javascript import folders_and_files
from ..javascript import dependences

#devuelve el nombre del archivo sin su sufijo 
def get_name_file(path):
    return PurePosixPath(path).stem

def get_name_file_with_suffix(path_file):
    return PurePosixPath(path_file).name

def valid(file):
    return file and PurePath(file.filename).suffix == folders_and_files.FILE_JS_EXTENSION

def upload(file,file_name):
    
    if not os.path.lexists(folders_and_files.CODES_PATH):
        os.makedirs(folders_and_files.CODES_PATH)
    
    if not file_name: 
        file = 'dafault_example'

    path = folders_and_files.CODES_PATH + file_name + folders_and_files.FILE_JS_EXTENSION
    
    if exist_file(file_name) and os.path.isfile(path):
        os.remove(path)
        
    file.save(path)
    return path

def exist_file(file_name):
    path = folders_and_files.CODES_PATH + file_name + folders_and_files.FILE_JS_EXTENSION
    return os.path.lexists(path)

def open_file(path):
    with open(path) as f:
        content = f.read()
        f.close()
    return content

def compile_js(path_file):
    command = 'node '+path_file
    return run_commands(command).stdout.read()

def run_test(path_file):
    #si no existen las dependecias las copia
    if not dependences.ok_dep(folders_and_files.CHALLENGES_PATH):
        cp_dependences = dependences.extract().stdout.read()

        if dependences.error_extract(cp_dependences): 
            return cp_dependences

    command_test = f'cd {folders_and_files.CHALLENGES_PATH}; npm test {path_file}' 
    test_ok = run_commands(command_test).stdout.read()
    # si no funciona los test instala las dependencias en la carpeta public
    if str(test_ok).find("Test Suites:") == -1:
        intall_dep = dependences.install().stdout.read()
        test_ok = run_commands(command_test).stdout.read()  
    return test_ok

def test_fail(output):
    return str(output).find('FAIL') != -1

def run_commands(command):
    return subprocess.Popen(command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT) 

def remove_files(*args): 
    for path_file in args:
        if os.path.lexists(path_file): os.remove(path_file)

def rename_file(path_file,file_new_name):
    
    if not os.path.isfile(file_new_name):
        file_new_name += folders_and_files.FILE_JS_EXTENSION
    
    directory = PurePosixPath(path_file).parent #devuelve el direcrorio padre del archivo
    new_path_file = directory.joinpath(file_new_name)
    os.rename(path_file, new_path_file)