import os

from flask import Flask, request
from flask_security import RoleMixin, UserMixin, SQLAlchemyUserDatastore, Security
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager,create_access_token, get_jwt_identity, jwt_required
from .db import db
from .routes import api, Demo, Login, DemoRequest, Register
from .session import SessionStore

# # from . import db
#
# db = SQLAlchemy()
# roles_users = db.Table('roles_users',
#         db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#         db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))
#
# class Role(db.Model, RoleMixin):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     description = db.Column(db.String(255))
#
# class User(db.Model, UserMixin):
#     fs_uniquifier = db.Column(db.String(64), unique=True)
#     id = db.Column(db.Integer, primary_key=True)
#     email = db.Column(db.String(255), unique=True)
#     password = db.Column(db.String(255))
#     active = db.Column(db.Boolean())
#     roles = db.relationship('Role', secondary=roles_users,
#                             backref=db.backref('users', lazy='dynamic'))

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
    # user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    # security = Security(app, user_datastore)

    api = Api(app)
    api.add_resource(Demo, '/demo')
    api.add_resource(Login,'/loginTrail')
    api.add_resource(DemoRequest,'/demoRequest')
    api.add_resource(Register,'/register')


    jwt = JWTManager(app)




    return app

# class demo(Resource):
#     def get(self):
#         return {'hello': 'world'}
#
# class login(Resource):
#     def __init__(self):
#         self.auth_data_parser = reqparse.RequestParser()
#         self.auth_data_parser.add_argument('email', type=str, required=True, help='email is needed')
#         self.auth_data_parser.add_argument('password', type=str, required=True, help='password is needed')
#
#     def post(self):
#         args = self.auth_data_parser.parse_args()
#         email = args['email']
#         password = args['password']
#         access_token = create_access_token(identity=email)
#         return { 'access_token':access_token}
#
# class demoRequest(Resource):
#     def __init__(self):
#         self.parser = reqparse.RequestParser()
#         self.parser.add_argument('access_token', type=str, required=True, help='access_token is needed')
#
#     @jwt_required()
#     def get(self):
#         current_user = get_jwt_identity()
#         return {"message": f"Hello, {current_user}"}



