
class CompileJSException(Exception):
    def __init__(self, msg, HTTP_code):
        self.msg = msg
        self.HTTP_code = HTTP_code
    def __str__(self):
        return repr(self.msg, self.HTTP_code)