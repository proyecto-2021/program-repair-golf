import subprocess

class Go_src:

    def __init__(self, path=None, file=None):
        self.path = path
        self.file = file

    def get_path(self):
        return self.path

    def get_file(self):
        return self.file

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

    def write_file(self, file_update):
        with open(self.get_file()) as f:
            with open(file_update, 'w') as file_to_update:
                for line in f:
                    file_to_update.write(line)

