
from .HTTPException import HTTPException
class ChallengeRepairException(HTTPException):
    def __init__(self, msg, HTTP_code):
        HTTPException.__init__(self, f"ChallengeRepairException: {msg}", HTTP_code)