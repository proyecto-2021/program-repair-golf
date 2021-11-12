import os, subprocess
from shutil import move, copy

class RubyCode:
    def __init__(self, full_name=None):
        self.path = None
        self.file_name = None
        self.file = None
        self.full_name = full_name
        if full_name is not None:
            self.path = os.path.dirname(full_name) + '/'
            self.file_name = os.path.basename(full_name).split('.')[0]
            self.file = None
            self.full_name = full_name

    def set_code(self, path, file_name, file=None):
        self.path = path
        self.file_name = file_name
        self.file = file
        self.full_name = path + file_name + '.rb'

    def get_path(self):
        return self.path

    def get_file_name(self):
        return self.file_name

    def get_full_name(self):
        return self.full_name

    def file_name_ok(self):
        return self.file_name and self.file_name == self.file_name.strip()

    def save(self):
        if os.path.isfile(self.get_full_name()):
            return False
        self.file.save(dst=self.get_full_name())
        return True

    def move(self, path, names_match=True):
        dst = path + self.get_file_name() + '.rb'
        if not names_match:
            if os.path.isfile(dst):
                return False
        self.full_name = move(self.get_full_name(), dst)
        self.path = path
        return True

    def copy(self, path):
        dst = path + self.get_file_name() + '.rb'
        return copy(self.get_full_name(), dst)

    def rename(self, new_name):
        os.rename(self.get_full_name(), self.path + new_name + '.rb')
        self.file_name = new_name
        self.full_name = self.path + new_name + '.rb'

    def remove(self):
        os.remove(self.get_full_name())

    def get_content(self):
        with open(self.get_full_name()) as f:
            return f.read()

    def compiles(self):
        command = 'ruby -c ' + self.get_full_name()
        return subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0

    def run_fail(self):
        command = 'ruby ' + self.get_full_name()
        return subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) != 0
