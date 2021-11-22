import os
import subprocess
import sys
from shutil import move, copy


class RubyCode:
    """Provide handling of the given code"""
    def __init__(self, full_name=None):
        """Initialize code with or without full name.
        
        Parameters:
            full_name (str): the name of the code with its path.

        Attributes:
            path (str): set where the file are stored,
            file_name (str): set the name of the code,
            file (FileStorage): content of the file,
            full_name (str): set the name of the code with its path.
        """
        self.path = None if full_name is None else os.path.dirname(full_name) + '/'
        self.file_name = None if full_name is None else os.path.basename(full_name).split('.')[0]
        self.full_name = full_name
        self.file = None

    def set_code(self, path, file_name, file=None):
        """Set the code attributes.

        Parameters:
            path (str): is where the files will be stored,
            file_name (str): the name of the file,
            file (FileStorage):  the content of the file.
        
        Attributes:
            path (str): set where the files will be stored,
            file_name (str): set name of the file,
            file (FileStorage): set the content of the file,
            full_name (str): set the full name of the file.
        """
        self.path = path
        self.file_name = file_name
        self.file = file
        if path and file_name:
            self.full_name = path + file_name + '.rb'

    def get_path(self):
        """Obtain the file path.

        Returns:
            path (str): get the file path.
        """
        return self.path

    def get_file_name(self):
        """Obtain the file name.

        Returns:
            file_name (str): get the file name.
        """
        return self.file_name

    def get_full_name(self):
        """Obtain the file full name.

        Returns:
            full_name (str): get the file full name.
        """
        return self.full_name

    def file_name_ok(self):
        """Check if the file name is valid.
        
        Returns:
            bool: confirmation that the file name is not empty or doesnt contain whitespace characters.
        """
        return self.file_name and self.file_name == self.file_name.strip()

    def save(self):
        """Try to save the file.

        Returns:
            bool: return true if the file could be saved and false if the file already exist.
        """
        if os.path.isfile(self.get_full_name()):
            return False
        self.file.save(dst=self.get_full_name())
        return True

    def move(self, path, names_match=True):
        """Move the file to a given path.

        Parameters:
            path (str): is where the files will be moved,
            names_match (bool): is a condition that if an element with the same name already exists,
            do not move this file.

        Returns:
            bool: report if the file could be moved or not.
        """
        dst = path + self.get_file_name() + '.rb'
        if not names_match:
            if os.path.isfile(dst):
                return False
        self.full_name = move(self.get_full_name(), dst)
        self.path = path
        return True

    def copy(self, path):
        """Create a new file equal to this file in the given path.

        Parameters:
            path (str): is where the files will be stored.

        Returns:
            str: the new file full name.
        """
        dst = path + self.get_file_name() + '.rb'
        return copy(self.get_full_name(), dst)

    def rename(self, new_name):
        """Change the file name.

        Parameters:
            new_name (str): the new name that the file will have.

        Attributes:
            file_name (str): is where the new name is stored,
            full_name (str): is where the new name is stored with the same path.
        """
        os.rename(self.get_full_name(), self.path + new_name + '.rb')
        self.file_name = new_name
        self.full_name = self.path + new_name + '.rb'

    def remove(self):
        """Delete the file"""
        os.remove(self.get_full_name())

    def get_content(self):
        """Obtain the file content.

        Returns:
            str: the content file.
        """
        with open(self.get_full_name()) as f:
            return f.read()

    def compiles(self):
        """Try to compile the code.

        Returns:
            bool: report if the file could be compiled or not.
        """
        command = 'ruby -c ' + self.get_full_name()
        return subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) == 0

    def run_fails(self):
        """Check that the file does not run correctly.

        Returns:
            bool: report if the file could not be executed.
        """
        command = 'ruby ' + self.get_full_name()
        return subprocess.call(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT) != 0


class RubyTestsCode(RubyCode):
    """Provide handling of the given test suite."""
    def dependencies_ok(self, code):
        """Check test suite dependencies match given code.

        Parameters:
            code (RubyCode): the code to which you want to apply the test suite.

        Returns:
            bool: report if the test suite can be apply to the code.
        """
        command = 'grep "require_relative" ' + self.get_full_name()
        p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        grep_return = p.communicate()[0].decode(sys.stdout.encoding)
        if grep_return.count('require_relative') != 1:
            return False
        dependence_name = (grep_return.strip().split("'")[1])
        return dependence_name == code.get_file_name()
