import os
from pathlib import PurePath, PurePosixPath

PUBLIC_PATH = './public/challenges/' 
FILE_EXTENSION = '.js'

def get_name_file(path):
    return PurePosixPath(path).stem

def valid(file):
    return  file and PurePath(file.filename).suffix == FILE_EXTENSION

def upload(file,file_name):
    
    if not os.path.lexists(PUBLIC_PATH):
        os.makedirs(PUBLIC_PATH)
    
    if not file_name: 
        file = 'dafault_example'

    path = PUBLIC_PATH + file_name + FILE_EXTENSION
    
    if exist_file(file_name) and os.path.isfile(path):
        os.remove(path)
        path = f'{PUBLIC_PATH + file_name}_upd{FILE_EXTENSION}'
        
    file.save(path)
    return path

def exist_file(file_name):
    path = PUBLIC_PATH + file_name + FILE_EXTENSION
    return os.path.lexists(path)

def open_file(path):
    with open(path) as f:
        content = f.read()
    return content