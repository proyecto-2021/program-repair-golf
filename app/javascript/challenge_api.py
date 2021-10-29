from app.javascript.models_js import JavascriptChallenge
from .. import db

#Class exclusive for consult BD
class challenge_api():

    def list(): #get
        return JavascriptChallenge.query.all() #JS o db?

    def listId(id): #get
        return JavascriptChallenge.query.filter_by(id = id).first() #JS o db?

    def create(#jsoin):
        db.session.add(challenge)
        db.session.commit()

    def update():
        db.session.commit()

    def remove(#json):
        db.session.delete()
        db.session.commit()