import subprocess, os, re

class Go_src:

    def __init__(self, path=None, file=None):
        self.path = path
        self.file = file
        #self.file_2 = file_2

    def get_path(self):
        return self.path

    def get_file(self):
        return self.file

    #def get_file_2(self):
    #    return self.file_2

    def set_path(self, path):
        self.path = path

    def code_compiles(self):
        return (subprocess.run(["go build"], cwd=os.path.abspath(re.sub('/\w+.go', '/', self.get_path())), stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode == 0

    def tests_compiles(self):
        return (subprocess.run(["go test -c"], cwd=os.path.abspath(re.sub('/\w+_\w+.go', '/', self.get_path())), stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode == 0   

    def tests_fail(self):
        return (subprocess.run(["go test"], cwd=os.path.abspath(re.sub('/\w+_\w+.go', '/', self.get_path())), stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode != 0

    def get_content(self):
        with open(self.get_path(),'r') as f:
            return f.read()

    def save(self):    
        self.file.save(self.get_path())

    def remove(self):
        os.remove(self.get_path())

    def write_file(self, file_update):
        with open(self.get_path()) as f:
            with open(file_update, 'w') as file_to_update:
                for line in f:
                    file_to_update.write(line)

    #def write_file_2(self):
    #    with open(self.get_file()) as f:
    #        with open(self.get_file_2()) as g:
    #            for line in f:
    #                g.write(line) 

path_code = Go_src(path='example-challenges/go-challenges/median.go')
path_test = Go_src(path='example-challenges/go-challenges/median_test.go')

#path_code.write_file('example-challenges/go-pruebas/aaa_test.go')
#path_test.remove()
print(path_code.code_compiles())
print(path_test.tests_compiles())
print(path_test.tests_fail())
