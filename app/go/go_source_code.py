import subprocess, os, re, shutil

class SourceCode:
    def __init__(self, path=None):
        self.path = path

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path
    
    def compiles(self, is_code):
        if is_code:
            path = os.path.abspath(re.sub('/\w+.go', '/', self.get_path()))
            command = "go build"
            return self.code_compiles(path, command)
        else:
            path = os.path.abspath(re.sub('/\w+_\w+.go', '/', self.get_path()))
            command = "go test -c"
            return self.tests_compiles(path, command)

    def code_compiles(self, path, command):
        return (subprocess.run([command], cwd = path, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode == 0

    def tests_compiles(self, path, command):
        return ((subprocess.run([command], cwd = path, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode != 1 and
        (subprocess.run([command], cwd = path, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode != 2 )

    def tests_fail(self):
        path_tests = os.path.abspath(re.sub('/\w+_\w+.go', '/', self.get_path()))
        return (subprocess.run(["go test"], cwd = path_tests, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode != 0

    def create_file(self):
        f = open(self.get_path(), 'x')
        f.close()

    def get_content(self):
        with open(self.get_path(),'r') as f:
            return f.read()

    def move(self, path):
        shutil.copy(path, self.get_path())

    def rewrite_file(self, path):
        with open(self.get_path(), 'r') as f:
                with open(path, 'w') as g:
                    for line in f:
                        g.write(line)