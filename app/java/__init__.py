from flask import Blueprint

java = Blueprint('java', __name__)

from . import views