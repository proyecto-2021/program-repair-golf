from . import client
from app import create_app, db
from app.cSharp.models import *
from app.cSharp.views import *
import pytest


def test get_challenge_from_db_without_files_contents(client):
    # Test get_challenge_db method with show_files_content=False
    pass
