import subprocess

class Go_src:

    def __init__(self, path, file_name, path_test):
        self.path = path
        self.name_file = file_name
        self.path_test = path_test
        #self.content_file = content_file

    def code_compiles(self):
        return subprocess.run(["go", "build", self.path], stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)

    def test_compiles(self):
        return subprocess.run(["go", "test", "-c"], cwd=self.path_test)

    def test_run(self):
        return subprocess.run(["go", "test"], cwd=self.path_test)