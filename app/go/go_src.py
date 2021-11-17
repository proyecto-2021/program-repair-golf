import subprocess, os, re, shutil

class Go_src:

    def __init__(self, path=None):
        self.path = path

    def get_path(self):
        return self.path

    def set_path(self, path):
        self.path = path

    def code_compiles(self):
        path_code = os.path.abspath(re.sub('/\w+.go', '/', self.get_path()))
        return (subprocess.run(["go build"], cwd=path_code, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode == 0

    def tests_compiles(self):
        path_test = os.path.abspath(re.sub('/\w+_\w+.go', '/', self.get_path()))
        return (subprocess.run(["go test -c"], cwd=path_test, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode != 1   

    def tests_fail(self):
        path_tests = os.path.abspath(re.sub('/\w+_\w+.go', '/', self.get_path()))
        return (subprocess.run(["go test"], cwd=path_tests, stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)).returncode != 0

    def create_file(self):
        f = open(self.get_path(), 'x')
        f.close()

    def write_file(self, string):
        with open(self.get_path(), 'w') as f:
            f.write(string)
            f.close()

    def get_content(self):
        with open(str(self.get_path()),'r') as f:
            return f.readlines()

    def save(self, file): 
        file.save()

    def create_dir(self):
        os.makedirs(self.get_path())

    def is_dir(self):
        return os.path.isdir(self.get_path())

    def create_path(parent_dir, directory):
        return os.path.join(parent_dir, directory)

    def remove_dir(self):
        shutil.rmtree(self.get_path())
    
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