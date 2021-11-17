from app.javascript.models.models_user import db

class JavascriptUser(db.model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(128), nullable = False )
    password = db.Column(db.String(128), nullable = False )
    attempts = db.Column(db.Integer)


    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "attempts": self.attempts
        }