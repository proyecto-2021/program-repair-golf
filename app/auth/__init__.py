from flask import Blueprint
from .userdao import get_user_by_name, get_user_by_id
from .password_encoding import check_password


def authenticate(username, password):
    user = get_user_by_name(username)
    if user and check_password(password.encode('utf-8'), user.password):
        return user
    return None


def identity(payload):
    user_id = payload['identity']
    return get_user_by_id(user_id)


users = Blueprint('users', __name__)

from . import views


