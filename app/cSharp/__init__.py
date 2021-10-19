from flask import Blueprint

cSharp = Blueprint('cSharp', __name__)

from . import views
