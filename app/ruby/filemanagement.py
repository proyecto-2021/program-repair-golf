from shutil import copy
import subprocess, os, sys
FILES_PATH = 'public/challenges/'

def delete_keys(dictionary, key_list):
    for key in key_list:
        del dictionary[key]

def save(file, path):
    if os.path.isfile(path):
        return False
    file.save(dst=path)
    return True

def file_exists(f):
    return os.path.isfile(f)

def update_file(challenge, file_type, source_path, source_name, data):
    if file_exists(source_path):
        os.remove(challenge[file_type])
        data[file_type] = copy(source_path, f"{FILES_PATH}{source_name}")
        os.remove(source_path)

def update_file_name(challenge, file_type, source_name, data):
    if (os.path.basename(challenge[file_type]) != source_name):
        new_name = f"{FILES_PATH}{source_name}"
        os.rename(challenge[file_type], new_name)
        data[file_type] = new_name

def compiles(file_name):
    command = 'ruby -c ' + file_name
    return (subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0)

def tests_fail(test_file_name):
    command = 'ruby ' + test_file_name
    return (subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) != 0)

def dependencies_ok(test_file_path, file_name):
    command = 'grep "require_relative" ' + test_file_path
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    dependence_name = (p.communicate()[0].decode(sys.stdout.encoding).strip().split("'")[1])
    return dependence_name == file_name
