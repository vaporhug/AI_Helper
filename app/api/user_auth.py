import time

from flask import jsonify, request
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from ..db import User,db
from ..utils import StandardResponse,RedisStore,send_verification_code,generate_verification_code

class SignIn(Resource):
    def __init__(self):
        self.auth_data_parser = reqparse.RequestParser()
        self.auth_data_parser.add_argument('email', type=str, required=True, help='email is needed')
        self.auth_data_parser.add_argument('password', type=str, required=True, help='password is needed')

    def post(self):
        args = self.auth_data_parser.parse_args()
        email = args['email']
        password = args['password'] # 这里有时间进行加密处理
        user = User.query.filter_by(email=email,password = password).first_or_404()
        
        if user is None:
            return StandardResponse(message='user not found',code=404)
        
        access_token = create_access_token(identity=email)
        return StandardResponse(data={'token':access_token})
        # time.sleep(2)


class SignUp(Resource):
    def __init__(self):
        self.auth_data_parser = reqparse.RequestParser()
        self.auth_data_parser.add_argument('email', type=str, required=True, help='email is needed')
        self.auth_data_parser.add_argument('password', type=str, required=True, help='password is needed')
        self.auth_data_parser.add_argument('username', type=str, required=True, help='username is needed')
        self.auth_data_parser.add_argument('gender', type=str, required=False, default='Not provided',
                                           help='gender is optional')
        self.auth_data_parser.add_argument('age', type=int, required=False, default=0, help='age is optional')
        self.auth_data_parser.add_argument('role', type=str, required=False, default='Not provided',
                                           help='role is optional')
    def post(self):
        args = self.auth_data_parser.parse_args()
        email = args['email']
        password = args['password']
        username = args['username']
        gender = args['gender']
        age = args['age']
        role = args['role']
        new_user = User(username=username, email=email, gender=gender, age=age, role=role, password=password)
        verify_code = generate_verification_code()
        RedisStore.add_register_info(new_user,verify_code())
        send_verification_code(email,verify_code)
        return StandardResponse()



class CheckCode(Resource): # ----------------
    def __init__(self):
        self.auth_data_parser = reqparse.RequestParser()
        self.auth_data_parser.add_argument('code', type=str, required=True, help='code is needed')
        self.auth_data_parser.add_argument('email', type=str, required=True, help='email is needed')

    def post(self):
        args = self.auth_data_parser.parse_args()
        code = args['code']
        email= args['email']

        if not RedisStore.register_info_exits(email):
            return StandardResponse(code=500,message='验证码已过期或未申请验证码')

        if code != RedisStore.get_verification_code(email):
            return StandardResponse(code=500,message='验证码错误,请重新输入')

        user:User = RedisStore.get_user_info(email)
        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=email)
        return StandardResponse(data={'token':access_token})


# class RequestSendVeriCode(Resource):
#     def __init__(self):
#         self.auth_data_parser = reqparse.RequestParser()
#         self.auth_data_parser.add_argument('token', type=str, required=True, )
#
#     def post(self):
#         args = self.auth_data_parser.parse_args()
#         token = args['token']
#         data = {
#             'code': 0,
#             'message': None,  # None或者不写此字段，dio解析到的就是null
#             'data': None
#         }
#         time.sleep(2)
#         return jsonify(data)


class UpdateUserInfo(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        # self.parser.add_argument('token', type=str, required=True)
        # self.parser.add_argument('name', type=str, required=False,)
        # self.parser.add_argument('birthday', type=str, required=False,)
        # self.parser.add_argument('gender', type=bool, required=False)
        # self.parser.add_argument('file', type=FileStorage, required=False)
        # self.parser.add_argument('role', type=int, required=False)
        # self.parser.add_argument('goal', type=int, required=False)

    def post(self):
        # args = self.parser.parse_args()
        token = request.form.get('token')
        name = request.form.get('name')
        birthday = request.form.get('birthday')
        gender = request.form.get('gender')
        img = request.files.get('avater')
        role = request.form.get('role')
        goal = request.form.get('goal')
        # 保存图片
        if img is not None:
            img.save('static/avatar' + img.filename)
            print(img)
        data = {
            'code': 0,
            'message': None,  # None或者不写此字段，dio解析到的就是null
            'data': None
        }
        time.sleep(2)
        return jsonify(data)