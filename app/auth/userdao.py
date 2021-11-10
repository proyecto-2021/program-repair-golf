from .usermodel import User
from app import db


def add_user(username, password):
    if get_user_by_name(username) is not None:
        raise ValueError(f'User with name {username} already in the DB')

    user = User(username=username, password=password)
    db.session.add(user)
    db.session.commit()


def get_user_by_name(name):
    return User.query.filter_by(username=name).first()