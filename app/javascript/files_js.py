import os
from pathlib import PurePath, PurePosixPath

PUBLIC_PATH = './public/challenges/' 
FILE_EXTENSION = '.js'


def valid(file):
    return  file and PurePath(file.filename).suffix == FILE_EXTENSION

def upload(file,file_name):
    
    if not os.path.lexists(PUBLIC_PATH):
        os.makedirs(PUBLIC_PATH)
    
    path = PUBLIC_PATH + file_name + FILE_EXTENSION
    
    if os.path.lexists(path) and os.path.isfile(path):
        os.remove(path)
        path = f'{PUBLIC_PATH + file_name}_upd{FILE_EXTENSION}'
        
    file.save(path)
    return path