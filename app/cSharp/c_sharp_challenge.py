from .c_sharp_src import CSharpSrc

class CSharpChallenge:

    def __init__(self, code, test, code_name, test_name, code_path=None, test_path=None):
        if code_path is not None:
            self.code = CSharpSrc(code, code_name, code_path)
        else:
            self.code = CSharpSrc(code, code_name)
        if test_path is not None:
            self.test = CSharpSrc(test, test_name, test_path)
        else:
            self.test = CSharpSrc(test, test_name)

    def validate(self):
        if self.code.compiles():
            if self.code.test_compiles(self.test):
                if self.code.tests_pass(self.test):
                    return 0
                else:
                    return 1
            else:
                return 2
        else:
            return -1