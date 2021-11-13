from .HTTPException import HTTPException
class challenge_dao_exception(HTTPException):
    def __init__(self,msg,HTTP_code):
        HTTPException.__init__(self,f"challenge_dao_exception:{msg}",HTTP_code)