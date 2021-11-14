import os
from werkzeug.datastructures import FileStorage
from pathlib import PurePath, PurePosixPath
from ..folders_and_files import FILE_JS_EXTENSION
from ..exceptions.FileUploadException import FileUploadException
from ..exceptions.FileReplaceException import FileReplaceException

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

def upload_file(file,file_path):
    directory = get_directory(file_path)
    name_file_upload = get_file(file_path)

    if not is_file_suffix(file, FILE_JS_EXTENSION):
        raise FileUploadException(f'the file is null or does not have a .js extension', FileUploadException.HTTP_NOT_FOUND)
        
    if not os.path.lexists(directory) and os.path.isdir(directory):
        os.makedirs(directory)
   
    if exist_file(file_path) and os.path.isfile(file_path):
        raise FileUploadException(f'The file {file_path} exist', FileUploadException.HTTP_CONFLICT)
        
    file.save(file_path)
    return file_path

def open_file(path):
    
    if not path: 
        return ""
    
    with open(path) as f:
        content = f.read()
        f.close()
    return content

def remove_files(*args): 
    for path_file in args:
        if os.path.lexists(path_file): 
            os.remove(path_file)

def replace_file(path_file,file_new_name):
    if not PurePath(path_file).suffix == PurePath(file_new_name).suffix:
        raise FileReplaceException(f'It is not possible to replace the {get_file(path_file)} file to {get_file(file_new_name)} the types are different', FileReplaceException.HTTP_NOT_FOUND)
    if not exist_file(path_file):
        print(path_file)
        raise FileReplaceException(f'file does not exist', FileReplaceException.HTTP_NOT_FOUND)
        
    new_path_file = file_new_name
    directory = get_directory(path_file)
    if exist_folder(file_new_name):
        new_path_file = directory.joinpath(file_new_name)
    os.rename(path_file, new_path_file)