import subprocess

class Go_src:

    def __init__(self, path, file_name, path_test):
        self.path = path
        self.name_file = file_name
        self.path_test = path_test

    def get_path(self):
        return self.path

    def get_file_name(self):
        return self.file_name

    def get_path_test(self):
        return self.path_test

    def code_compiles(self):
        return subprocess.run(["go", "build", self.path], stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)

    def test_compiles(self):
        return subprocess.run(["go", "test", "-c"], cwd=self.path_test)

    def test_run(self):
        return subprocess.run(["go", "test"], cwd=self.path_test)

    def content(self):
        f = open(self.path,'r')
        return f.read()
