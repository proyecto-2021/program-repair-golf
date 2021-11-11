from flask import Blueprint
from .userdao import get_user_by_name, get_user_by_id
from werkzeug.security import safe_str_cmp


def authenticate(username, password):
    user = get_user_by_name(username)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user
    return None


def identity(payload):
    user_id = payload['identity']
    return get_user_by_id(user_id)


users = Blueprint('users', __name__)

from . import views


