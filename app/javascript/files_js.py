import os
import subprocess
from pathlib import PurePath, PurePosixPath
import json

DEPENDENCES_FOLDER = './app/javascript/lib/'
PUBLIC_PATH = './public/challenges/'
CODE_FOLDER = "codes_challenges/"
FILE_EXTENSION = '.js'
CODE_PATH = PUBLIC_PATH + CODE_FOLDER

DEPENDENCES_FILES = {
    "modules_folder" : 'node_modules',
    "package_file" : 'package.json',
    "package_lock_file" : 'package-lock.json'
}

def get_name_file(path):
    return PurePosixPath(path).stem

def valid(file):
    return  file and PurePath(file.filename).suffix == FILE_EXTENSION

def upload(file,file_name):
    
    if not os.path.lexists(CODE_PATH):
        os.makedirs(CODE_PATH)
    
    if not file_name: 
        file = 'dafault_example'

    path = CODE_PATH + file_name + FILE_EXTENSION
    
    if exist_file(file_name) and os.path.isfile(path):
        os.remove(path)
        path = f'{CODE_PATH + file_name + FILE_EXTENSION}' # remplaza archivo

    file.save(path)
    return path

def exist_file(file_name):
    path = CODE_PATH + file_name + FILE_EXTENSION
    return os.path.lexists(path)

def open_file(path):
    with open(path) as f:
        content = f.read()
    return content

def compile_js(path_file):
    command = 'node '+path_file
    return run_commands(command).stdout.read()

def run_test(path_file):
    #si no existen las dependecias las copia
    if not ok_dependences():
        cp_dependences = extract_dependences().stdout.read()
        if cp_dependences: return cp_dependences

    command_test = f'cd {PUBLIC_PATH}; npm test {path_file}' 
    test_ok = run_commands(command_test).stdout.read()
    # si no funciona los test instala las dependencias en la carpeta public
    if str(test_ok).find("Test Suites:") == -1:
        intall_dep = install_dependence().stdout.read()
        test_ok = run_commands(command_test).stdout.read()  
    return test_ok

def test_fail(output):
    return str(output).find('FAIL') != -1

def extract_dependences():
    command = f'cd {DEPENDENCES_FOLDER}; unzip lib.zip -d ../../../{PUBLIC_PATH};'
    return run_commands(command) 

def install_dependence():
    command = f'cd {PUBLIC_PATH}; npm install'
    return run_commands(command)

def run_commands(command):
    return subprocess.Popen(command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT) 

def ok_dependences(): 
    return os.path.lexists(PUBLIC_PATH + DEPENDENCES_FILES['modules_folder']) and os.path.lexists(PUBLIC_PATH + DEPENDENCES_FILES["package_file"]) and os.path.lexists(PUBLIC_PATH + DEPENDENCES_FILES["package_lock_file"])

def rm_file(path_file):
    os.remove(path_file)

#! Estos metodos no son necesarios  

#inicia el package y instala jest,  
def intall_all_dependences():
    command = f'cd {PUBLIC_PATH}; npm init -y; npm install jest -D; '
    proc = subprocess.Popen(command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT) 
    #add_jest_int_test_value()
    return proc.stdout.read()

#remplaza el valor de test por jest en package.json y agregar entestEnvironment en la clave jest 
def add_jest_int_test_value(): 
    package_file = PUBLIC_PATH+'package.json'
    with open(package_file, 'r') as file:
        json_data = json.load(file)
        json_data['scripts']['test'] = "jest --verbose"
        json_data.update('jest', {"testEnvironment":"node"})
    with open(package_file, 'w') as file:
        json.dump(json_data, file, indent=2)