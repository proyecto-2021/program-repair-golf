from .c_sharp_src import CSharpSrc

class CSharpChallenge:

    def __init__(self, code, test, code_name, test_name, code_path, test_path):
        self.code = CSharpSrc(code, code_name, code_path)
        self.code.save()
        self.test = CSharpSrc(test, test_name, test_path)
        self.test.save()

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