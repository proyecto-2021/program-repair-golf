
class CommandRunException(Exception):
    def __init__(self,msj,HTTP_code):
        self.msj = msj
        self.HTTP_code = HTTP_code
    def __str__(self):
        return repr(self.msj, self.HTTP_code)