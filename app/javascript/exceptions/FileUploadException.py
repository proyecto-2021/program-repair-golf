
from .HTTPException import HTTPException
class FileUploadException(HTTPException):
    def __init__(self, msg, HTTP_code):
        HTTPException.__init__(self, f"FileUploadException: {msg}", HTTP_code) 
