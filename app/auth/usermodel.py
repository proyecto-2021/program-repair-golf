from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password
        }
