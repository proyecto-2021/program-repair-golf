import os
from tempfile import gettempdir

class Config(object):
    TESTING = False
    FILES_PATH = 'public/challenges/'

    @staticmethod
    def init_app(app):
        pass

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = "sqlite:////tmp/foo.db"

class TestingConfig(Config):
    FILES_PATH = gettempdir() + '/'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
