class HTTPException(Exception):

    HTTP_OK = 200
    HTTP_NOT_FOUND = 404
    HTTP_CONFLICT = 409
    HTTP_INTERNAL_SERVER_ERROR = 500

    def __init__(self, msg, HTTP_code):
        self.msg = msg
        self.HTTP_code = HTTP_code
    def __str__(self):
        return repr(self.msg, self.HTTP_code)
