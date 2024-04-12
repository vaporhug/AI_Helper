# from app.utils import SessionStore
#
# session = SessionStore()
#
# session.initialize_connection()
#
# session.add_interaction("token","hello,server","hello,client")
# session.add_interaction("token","hello,server1","hello,client1")
# data =  session.get_interaction("token")
#
# print(data['requests'][1])

# from app.utils import get_text_from_picture_rb
# from PIL import Image
#
# # 调用函数
# image = Image.open('img.png')
# data = get_text_from_picture_rb(image)
# print(data)

# from flask_jwt_extended import create_access_token,JWTManager
# from flask import Flask
# app = Flask(__name__)
# app.config['JWT_SECRET_KEY'] = 'super-secret'  # 设置密钥，实际应用中应该更安全
#
# jwt = JWTManager(app)
# with app.app_context():
#     email = 'user@example.com'
#     access_token = create_access_token(identity=email)
#     print(access_token)

# import os
# from app.utils import send_verification_code
# print(os.getenv('EMAIL_TYPE'),os.getenv('EMAIL_ACCOUNT'),os.getenv('EMAIL_PASSWORD'))
# send_verification_code("3253034317@qq.com","123456")
#
# from app.utils import conver_markdow2pdf
# conver_markdow2pdf('test.md','static/note/','test.pdf')
# from app.utils import RedisStore
#
# RedisStore.initialize_connection()
# r = RedisStore.get_redis_connection()
# RedisStore.add_user_file('user','file1')
# values = r.smembers('file_set_user')
# for value in values:
#     print(value.decode('utf-8'))  # 输出值
# RedisStore.add_user_file('user','file2')
# print(r.smembers('file_set_user'))
# RedisStore.delete_user_file('user','file1')
# print(r.smembers('file_set_user'))
# RedisStore.delete_user_file('user','file1')
# print(r.smembers('file_set_user'))
# RedisStore.delete_user_file('user','file2')
# print(r.smembers('file_set_user'))
import hashlib
from app.utils import *
def generate_content_hash(content):
    # 创建一个md5 hash对象
    hash_object = hashlib.md5(content.encode())
    # 获取16进制的哈希值
    hex_dig = hash_object.hexdigest()
    return hex_dig

id = 'user'
FILE_LIEF_TIME = 10
FILES_DIRECTORY = 'static/note/'
# 使用示例
markdown_text = """# Welcome to My Project

## Introduction

This is a sample project. It's purpose is to demonstrate the conversion of Markdown to PDF.

## Features

- Feature 1
- Feature 2
- Feature 3

## Conclusion

Thank you for using this sample project!"""
hash_object = hashlib.md5(markdown_text.encode())
content_hash = hash_object.hexdigest()
markdown_file_path = FILES_DIRECTORY+str(id)+'/note'+str(content_hash)+'.md'
pdf_file_path = FILES_DIRECTORY+str(id)+'/note'+str(content_hash)+'.pdf'
print(1)
directory = os.path.dirname(markdown_file_path)
print(2)
if not os.path.exists(directory):
    os.makedirs(directory)
print(3)
with open(markdown_file_path, 'w') as f:
     f.write(markdown_text)
print(4)
conver_markdow2pdf(markdown_file_path,pdf_file_path)
print(5)
delete_file_after_delay(markdown_file_path,FILE_LIEF_TIME)
delete_file_after_delay(pdf_file_path,FILE_LIEF_TIME)
        # 保存图片
