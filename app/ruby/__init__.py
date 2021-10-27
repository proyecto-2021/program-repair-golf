from flask import Blueprint

ruby = Blueprint('ruby',__name__)

from . import RubyChallengeAPI
