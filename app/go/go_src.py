import subprocess, os, re, shutil

class Go_src:

    def __init__(self, path=None):
        self.path = path

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path
    
    def code_compiles(self, path, command):
        return (subprocess.run([command], cwd = path, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode == 0

    def tests_compiles(self, path, command):
        return (subprocess.run([command], cwd = path, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode != 1  

    def compiles(self, is_code):
        if is_code:
            path = os.path.abspath(re.sub('/\w+.go', '/', self.get_path()))
            command = "go build"
            return self.code_compiles(path, command)
        else:
            path = os.path.abspath(re.sub('/\w+_\w+.go', '/', self.get_path()))
            command = "go test -c"
            return self.tests_compiles(path, command)

    def tests_fail(self):
        path_tests = os.path.abspath(re.sub('/\w+_\w+.go', '/', self.get_path()))
        return (subprocess.run(["go test"], cwd = path_tests, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode != 0

    def create_file(self):
        f = open(self.get_path(), 'x')
        f.close()

    def write_file(self, string):
        with open(self.get_path(), 'w') as f:
            f.write(string)
            f.close()

    def get_content(self):
        with open(self.get_path(),'r') as f:
            return f.readlines()

    def move(self, path):
        shutil.copy(path, self.path)

    def save(self, file): 
        file.save(self.get_path())
    
    def remove_file(self):
        os.remove(self.get_path())

    def delete_files(self):
        for file in os.listdir(self.get_path()):
            os.remove(os.path.join(self.get_path(), file))

    def rewrite_file(self, update_data):
        with open(self.get_path(), 'w') as f:
                with open(update_data, 'r') as g:
                    for line in g:
                        f.write(line)

    def create_file_tmp(path, name, file):
        path_to_file = Go_src(path = path.get_path() + name)
        file.save(path_to_file.get_path())
        return path_to_file