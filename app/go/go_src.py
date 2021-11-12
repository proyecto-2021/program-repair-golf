import subprocess, os

class Go_src:

    def __init__(self, path=None, file=None, file_2=None):
        self.path = path
        self.file = file
        self.file_2 = file_2

    def get_path(self):
        return self.path

    def get_file(self):
        return self.file

    def get_file_2(self):
        return self.file_2

    def set_path(self, new_path):
        self.path = new_path

    def code_compiles(self):
        return (subprocess.run(["go", "build", self.get_path()], stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL)).returncode == 0

    def test_compiles(self):
        return (subprocess.run(["go", "test", "-c"], cwd=self.get_path())).returncode == 0

    def test_run(self):
        return (subprocess.run(["go", "test"], cwd=self.get_path())).returncode == 0

    def remove_file(self):
        return subprocess.run(["rm" "-r" "solution"],cwd=os.path.abspath(self.get_path),stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)

    def generic_compile(self, command, path):
        return subprocess.run(command, cwd=os.path.abspath(self.get_path()),stderr=subprocess.STDOUT, stdout=subprocess.DEVNULL, shell=True)

    def get_content(self):
        with open(self.get_path(),'r') as f:
            return f.read()

    def save(self):
        self.file.save(self.get_path())

    def remove(self):
        os.remove(self.get_path())

    def write_file(self, file_update):
        with open(self.get_file()) as f:
            with open(file_update, 'w') as file_to_update:
                for line in f:
                    file_to_update.write(line)

    def write_file_2(self):
        with open(self.get_file()) as f:
            with open(self.get_file_2()) as g:
                for line in f:
                    g.write(line) 

