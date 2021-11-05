from .HTTPException import HTTPException
class dao_get_challenge_exception(HTTPException):
    def __init__(self,msg,HTTP_code):
        HTTPException.__init__(self,f"dao_get_challenge_exception:{msg}",HTTP_code)