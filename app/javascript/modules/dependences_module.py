import os
import json
from .command_module import run_command, run_command_ok, command_output
from ..exceptions.CommandRunException import CommandRunException
from ..folders_and_files import DEPENDENCES_PAKCAGUE_PATH,CHALLENGES_PATH,DEP_MODULES_FOLDER,DEP_PACKAGE_JSON_FILE,DEP_PACKAGE_LOCK_JSON_FILE,CHALLENGES_FOLDER

def extract_dependences(path):
    command = f'unzip {DEPENDENCES_PAKCAGUE_PATH} -d {path};'
   
    if not dependences_ok(path):
        proc = run_command(command) 
        if not run_command_ok(proc):
            raise CommandRunException(f"Extract Dependences Error:{ command }",CommandRunException.HTTP_NOT_FOUND)
        return command_output(proc)
    return ''

def install_dependece(path):
    command = f'cd {path}; npm install'
    proc = run_command(command)
    if not run_command_ok(proc):
        raise CommandRunException(f"Install Dependes Error:{ command }",CommandRunException.HTTP_NOT_FOUND)
    return command_output(proc)

def error_extract(output): 
    error_open = 'cannot'
    return str(output).find(error_open) != -1 

def dependences_ok(directory): 
    return os.path.lexists(directory + DEP_MODULES_FOLDER) and os.path.lexists(directory + DEP_PACKAGE_JSON_FILE) and os.path.lexists(directory + DEP_PACKAGE_LOCK_JSON_FILE)


#Inicia el package y instala jest,  
def install_all_dependences(path):
    command = f'cd {path}; npm init -y; npm install jest -D; '
    proc = run_command(command)
    if not run_command_ok(proc):
        raise CommandRunException(f"Install all Dependences Error:{ command }",CommandRunException.HTTP_NOT_FOUND)
    return command_output(proc)

def remove_dependences(path):
    command = f'cd {path}; rm -rf {DEP_MODULES_FOLDER} {DEP_PACKAGE_JSON_FILE} {DEP_PACKAGE_LOCK_JSON_FILE}'
    proc = run_command(command)
    if not run_command_ok(proc):
        raise CommandRunException(f"Remove Dependes Error:{ command }",CommandRunException.HTTP_NOT_FOUND)
    return command_output(proc)

#Remplaza el valor de test por jest en package.json y agregar entestEnvironment en la clave jest 
def add_jest_int_test_value(path): 
    package_file = path + DEP_PACKAGE_JSON_FILE
    with open(package_file, 'r') as file:
        json_data = json.load(file)
        json_data['scripts']['test'] = "jest --verbose"
        json_data.update('jest', {"testEnvironment":"node"})
    with open(package_file, 'w') as file:
        json.dump(json_data, file, indent=2)