from flask import Blueprint

javascript = Blueprint('javascript', __name__)

from .api import javascript_challenge_api