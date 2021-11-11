import subprocess

class Go_src:

    def __init__(self, path, file=None):
        self.path = path

    def get_path(self):
        return self.path

    #def get_file_name(self):
    #    return self.file_name

    #def get_path_test(self):
    #    return self.path_test

    def code_compiles(self):
        return subprocess.run(["go", "build", self.get_path()], stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)

    def test_compiles(self):
        return subprocess.run(["go", "test", "-c"], cwd=self.get_path())

    def test_run(self):
        return subprocess.run(["go", "test"], cwd=self.get_path())

    def get_content(self):
        f = open(self.get_path(),'r')
        return f.read()

    def save(self):
        self.file.save(self.get_path())

    def remove(self):
        os.remove(get_path())

    #def write(self):
    #    ...

