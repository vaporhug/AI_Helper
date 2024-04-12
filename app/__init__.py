import os
from flask import Flask
from flask_restful import Api
from .db import db
from .utils import SessionStore
from .api import init_api


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
    )
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost/AI_Helper_DataBase'
    app.config['SECRET_KEY'] = 'super-secret'
    app.config['SECURITY_PASSWORD_SALT'] = 'salt'
    app.config["JWT_SECRET_KEY"] = "super-secret"
    SessionStore.initialize_connection()


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    ############
    db.init_app(app)
    with app.app_context():
        db.create_all()
    api = Api(app)
    init_api(api)

    return app
