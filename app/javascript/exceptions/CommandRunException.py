from .HTTPException import HTTPException
class CommandRunException(HTTPException):
    def __init__(self, msj, HTTP_code):
        HTTPException.__init__(self, f"CommandRunException: {msj}", HTTP_code)
