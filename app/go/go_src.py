import subprocess, os, re, shutil

class Go_src:

    def __init__(self, path=None, file=None):
        self.path = path
        self.file = file

    def get_path(self):
        return self.path

    def get_file(self):
        return self.file

    def set_path(self, path):
        self.path = path

    def code_compiles(self):
        path_code = os.path.abspath(re.sub('/\w+.go', '/', self.get_path()))
        return (subprocess.run(["go build"], cwd=path_code, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode == 0

    def tests_compiles(self):
        path_test = os.path.abspath(re.sub('/\w+_\w+.go', '/', self.get_path()))
        return (subprocess.run(["go test -c"], cwd=path_test, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode == 0   

    def tests_fail(self):
        path_tests = os.path.abspath(re.sub('/\w+_\w+.go', '/', self.get_path()))
        return (subprocess.run(["go test"], cwd=path_tests, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode != 0

    def get_content(self):
        with open(self.get_path(),'r') as f:
            return f.read()

    def save(self):    
        self.file.save(self.get_path())

    def create_dir(self):
        os.makedirs(self.get_path())

    def is_dir(self):
        os.path.isdir(self.get_path())

    def create_path(self, path, directory):
        return os.path.join(path, directory)

    def remove_dir(self):
        shutil.rmtree(self.get_path())
    
    def remove_file(self):
        os.remove(self.get_path())

    def rewrite_file(self, update_data):
        with open(self.get_path(), 'w') as f:
                with open(update_data, 'r') as g:
                    for line in g:
                        f.write(line)