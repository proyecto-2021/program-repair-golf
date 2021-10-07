from flask import Blueprint

go = Blueprint('go', __name__)

from . import views