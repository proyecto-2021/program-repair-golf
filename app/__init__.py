from flask import Flask
from config import config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    config[config_name].init_app(app)

    from .models import User, Role
    from .javascript.models_js import JavascriptChallenge 
    from .ruby.rubychallengemodel import RubyChallengeModel
    from .java.models_java import Challenge_java
    from .cSharp.models import CSharp_Challenge
    from .go.models_go import GoChallenge
    from .python.models import PythonChallengeModel

    db.init_app(app)
    migrate.init_app(app, db)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .javascript import javascript as javascript_blueprint
    app.register_blueprint(javascript_blueprint, url_prefix='/javascript')  

    from .java import java as java_blueprint
    app.register_blueprint(java_blueprint, url_prefix='/java')

    from .ruby import ruby as ruby_blueprint
    app.register_blueprint(ruby_blueprint, url_prefix='/ruby')

    from .go import go as go_blueprint
    app.register_blueprint(go_blueprint, url_prefix='/go')

    from .python import python as python_blueprint
    app.register_blueprint(python_blueprint, url_prefix='/python')

    from .cSharp import cSharp as cSharp_blueprint
    app.register_blueprint(cSharp_blueprint, url_prefix='/cSharp')

    return app
