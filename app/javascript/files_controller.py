import os
from werkzeug.datastructures import FileStorage
import subprocess
from pathlib import PurePath, PurePosixPath
import json
from ..javascript import folders_and_files
from ..javascript import dependences

#devuelve el nombre del archivo sin su sufijo 
def get_name_file(path):
    return PurePosixPath(path).stem

def get_file(file_path):
    return PurePosixPath(file_path).name

def get_directory(file_path):
    return PurePosixPath(file_path).parent

def is_file_suffix(file_path, suffixs):
    if type(file_path) == FileStorage:
        file_path = file_path.filename    
    return file_path and PurePath(file_path).suffix == suffixs

def exist_folder(directory):
    return os.path.lexists(directory) and os.path.isdir(directory)

def to_temp_file(path_file):
    name_file = get_name_file(path_file).split(".")[0]
    rep = path_file.replace(name_file, f'{name_file}_tmp')
    return rep

def exist_file(file_path):
    return os.path.lexists(file_path) and os.path.isfile(file_path) 

def upload(file,file_path):
    directory = get_directory(file_path)
    name_file_upload = get_file(file_path)

    if not os.path.lexists(directory) and os.path.isdir(directory):
        os.makedirs(directory)
   
    if exist_file(file_path) and os.path.isfile(file_path):
        os.remove(file_path)
        
    file.save(file_path)
    return file_path

def open_file(path):
    
    if not path: 
        return ""
    
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
        if os.path.lexists(path_file): 
            os.remove(path_file)

def rename_file(path_file,file_new_name):
    if PurePath(path_file).suffix == PurePath(file_new_name).suffix:
        new_path_file = file_new_name
        directory = get_directory(path_file)
        if exist_folder(file_new_name):
            new_path_file = directory.joinpath(file_new_name)
        os.rename(path_file, new_path_file)