from .password_encoding import hash_password
from .usermodel import User
from app import db


def add_user(username, password):
    if get_user_by_name(username) is not None:
        raise ValueError(f'User with name {username} already in the DB')

    encoded_pass = hash_password(password.encode('UTF-8'))
    user = User(username=username, password=encoded_pass)
    db.session.add(user)
    db.session.commit()


def get_user_by_name(name):
    return User.query.filter_by(username=name).first()


def get_all_users():
    return User.query.all()


def get_user_by_id(user_id):
    return User.query.filter_by(id=user_id).first()


def remove_user_by_id(user_id):
    stored_id = get_user_by_id(user_id)
    if stored_id is not None:
        User.query.filter_by(id=user_id).delete()
        db.session.commit()
        return True

    return False
