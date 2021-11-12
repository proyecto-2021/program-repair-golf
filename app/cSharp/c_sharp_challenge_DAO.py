from app.cSharp.models import CSharpChallengeModel
from app import db

class CSharpChallengeDAO:

    def __init__(self):
        pass

    def exist(self, id):
        return db.session.query(CSharpChallengeModel).filter_by(id=id).first() is not None