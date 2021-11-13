
from .HTTPException import HTTPException
class FileReplaceException(HTTPException):
    def __init__(self, msg, HTTP_code):
        HTTPException.__init__(self, f"FileReplaceException: {msg}", HTTP_code)