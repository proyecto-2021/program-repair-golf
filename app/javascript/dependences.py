import os
import subprocess
from ..javascript import folders_and_files

def extract():
    command = f'unzip {folders_and_files.DEPENDENCES_PAKCAGUE_PATH} -d {folders_and_files.CHALLENGES_PATH};'
    print(command)
    return run_commands(command) 

def install():
    command = f'cd {folders_and_files.CHALLENGES_PATH}; npm install'
    return run_commands(command)

def error_extract(output): 
    error_open = 'cannot'
    return str(output).find(error_open) != -1 

def ok_dep(directory): 
    return os.path.lexists(directory + folders_and_files.DEP_MODULES_FOLDER) and os.path.lexists(directory + folders_and_files.DEP_PACKAGE_JSON_FILE) and os.path.lexists(directory + folders_and_files.DEP_PACKAGE_LOCK_JSON_FILE)

def run_commands(command):
    return subprocess.Popen(command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT) 

#! Estos metodos no son necesarios  
#inicia el package y instala jest,  
def intall_all_dependences():
    command = f'cd {folders_and_files.CHALLENGES_PATH}; npm init -y; npm install jest -D; '
    proc = subprocess.Popen(command, shell=True, stdout = subprocess.PIPE, stderr = subprocess.STDOUT) 
    #add_jest_int_test_value()
    return proc.stdout.read()

#remplaza el valor de test por jest en package.json y agregar entestEnvironment en la clave jest 
def add_jest_int_test_value(): 
    package_file = folders_and_files.CHALLENGES_FOLDER + folders_and_files.DEP_PACKAGE_JSON_FILE
    with open(package_file, 'r') as file:
        json_data = json.load(file)
        json_data['scripts']['test'] = "jest --verbose"
        json_data.update('jest', {"testEnvironment":"node"})
    with open(package_file, 'w') as file:
        json.dump(json_data, file, indent=2)