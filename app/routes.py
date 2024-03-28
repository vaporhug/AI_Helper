from flask import request
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from sqlalchemy_utils.types import password

from .db import db
from .db import User

api = Api()

class Demo(Resource):
    def get(self):
        return {'hello': 'world'}

class Login(Resource):
    def __init__(self):
        self.auth_data_parser = reqparse.RequestParser()
        self.auth_data_parser.add_argument('email', type=str, required=True, help='email is needed')
        self.auth_data_parser.add_argument('password', type=str, required=True, help='password is needed')

    def post(self):
        args = self.auth_data_parser.parse_args()
        email = args['email']
        password = args['password']
        access_token = create_access_token(identity=email)
        return { 'access_token':access_token}

class DemoRequest(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('access_token', type=str, required=True, help='access_token is needed')

    @jwt_required()
    def get(self):
        current_user = get_jwt_identity()
        return {"message": f"Hello, {current_user}"}

class Register(Resource):
    def __init__(self):
        self.register_data_parser = reqparse.RequestParser()
        self.register_data_parser.add_argument('username', type=str, required=True, help='username is needed')
        self.register_data_parser.add_argument('email', type=str, required=True, help='email is needed')
        self.register_data_parser.add_argument('gender', type=str, required=True, help='gender is needed')
        self.register_data_parser.add_argument('age', type=int, required=True, help='age is needed')
        self.register_data_parser.add_argument("password", type=str, required=True, help='password is needed')
        self.register_data_parser.add_argument('role', type=str, required=True, help='role is needed')

    def post(self):
        args = self.register_data_parser.parse_args()
        username = args['username']
        email = args['email']
        gender = args['gender']
        age = args['age']
        role = args['role']
        password = args['password']

        # 创建新用户
        new_user = User(username=username, email=email, gender=gender, age=age, role=role,password=password)

        # 将新用户添加到数据库
        db.session.add(new_user)
        db.session.commit()

        return {'message': 'User registered successfully'}

class Conversation(Resource):
    def __init__(self):
        self.register_data_parser = reqparse.RequestParser()

