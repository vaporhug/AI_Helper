import time
import hashlib
from flask_jwt_extended import  get_jwt_identity, jwt_required
from flask import jsonify, request
from flask_restful import Resource, reqparse
from flask import  send_from_directory, abort
from werkzeug.security import safe_join
from app.utils import conver_markdow2pdf,get_text_from_picture_rb,delete_file_after_delay,StandardResponse
from app.db import User
import os

FILES_DIRECTORY = 'static/note/'

REQUEST_PREFIX = os.getenv('LOCAL_HOST')+'note/' # LOCAL_HOST:http://192.168.5.101:8091/

FILE_LIEF_TIME = 60

class GetNoteFileURL(Resource):
    def __init__(self):
        pass
    @jwt_required
    def post(self):
        file = request.files.get('file')
        user: User = User.query.filter_by(email=get_jwt_identity()).first()
        markdown_text = get_text_from_picture_rb(file)
        hash_object = hashlib.md5(markdown_text.encode())
        content_hash = hash_object.hexdigest()
        markdown_file_path = FILES_DIRECTORY+str(user.id)+'/note'+str(content_hash)+'.md'
        pdf_file_path = FILES_DIRECTORY+str(user.id)+'/note'+str(content_hash)+'.pdf'

        directory = os.path.dirname(markdown_file_path)
        print(2)
        if not os.path.exists(directory):
            os.makedirs(directory)

        with open(markdown_file_path, 'w') as f:
            f.write(markdown_text)
        conver_markdow2pdf(markdown_file_path,pdf_file_path)
        delete_file_after_delay(markdown_file_path,FILE_LIEF_TIME)
        delete_file_after_delay(pdf_file_path,FILE_LIEF_TIME)
        # 保存图片
        if file is not None:
            file.save('static/note' + file.filename)
            delete_file_after_delay('static/note' + file.filename, FILE_LIEF_TIME)

        return StandardResponse(data={'url':pdf_file_path}).to_dict()


class getNoteFile(Resource):
    def get(self, filename):
        try:
            # 确保文件路径安全，防止路径遍历
            safe_path = safe_join(FILES_DIRECTORY, filename)
            # 检查文件是否真实存在
            if not os.path.exists(safe_path):
                # 如果文件不存在，返回404错误
                abort(404)
            # 从安全路径发送文件
            return send_from_directory(FILES_DIRECTORY, filename, as_attachment=True)
        except FileNotFoundError:
            abort(404)