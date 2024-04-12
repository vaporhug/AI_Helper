# ——————————————————————————————————————————这里是封装返回给前端的回复的格式——————————————————————————————————————————————


class StandardResponse:
    def __init__(self, message="success", code=200, data=None):
        if data is None:
            data = {}
        self.message = message
        self.code = code
        self.data = data

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
            'data': self.data
        }
def make_standard_response(user_token="", status_code=200, content=None):
    response = StandardResponse(user_token, status_code, content)
    return jsonify(response.to_dict()), status_code

# ————————————————————————————————————————————————————————管理用户的对话的上下文的信息的组件————————————————————————————————————
from flask import jsonify
import redis
from app.db import User
import pickle

class RedisStore:
    # 静态变量用于存储 Redis 连接
    __redis_connection = redis.StrictRedis(host='localhost', port=6379, db=0)# 在这个初始化不知道有无问题

    @staticmethod
    def initialize_connection(host='localhost', port=6379, db=0):
        """
        初始化 Redis 连接并存储到静态变量中。

        参数:
        host -- Redis 服务器的主机名
        port -- Redis 服务器的端口号
        db -- Redis 数据库的索引号
        """
        RedisStore.__redis_connection = redis.Redis(host=host, port=port, db=db)

    @staticmethod
    def get_redis_connection():
        """
        获取存储的 Redis 连接。

        返回:
        返回 Redis 连接实例
        """
        if RedisStore.__redis_connection is None:
            raise Exception("Redis connection is not initialized. Please call 'initialize_connection' first.")
        return RedisStore.__redis_connection

    @staticmethod
    def add_interaction(session_id, user_request, server_response):
        """
        将用户请求和服务器响应添加到 Redis 中对应的会话。

        参数:
        redis_connection -- 活动的 Redis 连接实例
        session_id -- 会话的唯一标识符
        user_request -- 用户的请求内容
        server_response -- 服务器的响应内容
        """
        redis_connection = RedisStore.get_redis_connection()
        redis_connection.rpush(f'session:{session_id}:requests', user_request)
        redis_connection.rpush(f'session:{session_id}:responses', server_response)

    @staticmethod
    def add_register_info(user:User,verification_code):
        """
        将用户请求和服务器响应添加到 Redis 中对应的会话。

        参数:
        redis_connection -- 活动的 Redis 连接实例
        session_id -- 会话的唯一标识符
        user_request -- 用户的请求内容
        server_response -- 服务器的响应内容
        """
        redis_connection = RedisStore.get_redis_connection()
        obj_bytes = pickle.dumps(user)
        redis_connection.rpush(User.email, obj_bytes, verification_code)

    @staticmethod
    def register_info_exits(email):
        redis_connection = RedisStore.get_redis_connection()
        return redis_connection.exists(email)

    @staticmethod
    def get_verification_code(email):
        redis_connection = RedisStore.get_redis_connection()
        verification_code = redis_connection.lindex(email, 1).decode('utf-8')
        return verification_code

    @staticmethod
    def get_user_info(email):
        redis_connection = RedisStore.get_redis_connection()
        object_byte = redis_connection.lindex(email, 0)
        user:User = pickle.loads(object_byte)
        return user

    @staticmethod
    def get_interaction( session_id):
        """
        获取指定会话 ID 的用户请求和服务器响应。

        参数:
        redis_connection -- 活动的 Redis 连接实例
        session_id -- 会话的唯一标识符

        返回:
        一个字典，包含请求和响应列表
        """
        redis_connection = RedisStore.get_redis_connection()
        requests = redis_connection.lrange(f'session:{session_id}:requests', 0, -1)
        responses = redis_connection.lrange(f'session:{session_id}:responses', 0, -1)
        requests = [req.decode('utf-8') for req in requests]
        responses = [resp.decode('utf-8') for resp in responses]
        return {'requests': requests, 'responses': responses}

    @staticmethod
    def delete_session(session_id):
        """
        删除指定会话 ID 的所有数据。

        参数:
        redis_connection -- 活动的 Redis 连接实例
        session_id -- 会话的唯一标识符
        """
        redis_connection = RedisStore.get_redis_connection()
        redis_connection.delete(f'session:{session_id}:requests')
        redis_connection.delete(f'session:{session_id}:responses')

    @staticmethod
    def add_user_file(user_id,file_name):
        redis_connection = RedisStore.get_redis_connection()
        redis_connection.sadd('file_set_' + user_id, file_name)
    @staticmethod
    def delete_user_file(user_id, file_name):
        redis_connection = RedisStore.get_redis_connection()
        if redis_connection.scard('file_set_' + user_id) == 1:
            redis_connection.delete('file_set_' + user_id)
            return
        redis_connection.srem('file_set_' + user_id, file_name)

# ————————————————————————————————————————————合合信息的api的请求————————————————————————————————————————————————————
import requests
import io

# API端点
url = 'https://api.textin.com/ai/service/v2/recognize'

# 替换这里的值为您从API提供方获取的实际值
x_ti_app_id = 'fb6b6064f0cec83cbad2f75b0ae69232'
x_ti_secret_code = '8d78745fa363046eb8c8f3300d59b1ef'

# 请求头部
headers = {
    'x-ti-app-id': x_ti_app_id,
    'x-ti-secret-code': x_ti_secret_code
}

# URL参数
# 根据API要求，这里可以设置为0或1，修改为所需的值
params = {
    'character': 0,  # 是否返回完整的字符信息
    'straighten': 0,  # 是否返回以正置图像作为参照系的坐标点
}


def get_text_from_picture_rb(img_file):
    # 将图片文件转换为字节对象
    img_byte_array = io.BytesIO()
    img_file.save(img_byte_array, format='PNG')
    img_byte_array = img_byte_array.getvalue()

    # 发送HTTP POST请求
    response = requests.post(url, headers=headers, params=params, data=img_byte_array)
    if response.status_code == 200:
        # 解析响应体为JSON
        data = response.json()
        text = ''
        for item in data['result']['lines']:
            text += item['text'] + '\n'
        return text
    else:
        print(response)
        raise Exception(f'exception from get_text_from_picture_rb')
# ————————————————————————————————————————————验证码————————————————————————————————————————————————————
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import os

def generate_verification_code():
    import random
    return ''.join([random.choice('0123456789') for _ in range(6)])
def send_verification_code(email,verification_code):
    email_content = f"""
        尊敬的用户，

        您正在进行邮箱验证，您的验证码为：

        {verification_code}

        请在提交验证码页面输入此验证码以完成验证。

        如果您没有进行此操作，请忽略此邮件。

        此致，

        您的团队
        """
    send_email(smtp_server = os.getenv('EMAIL_TYPE'), sender_password = os.getenv('EMAIL_PASSWORD'),sender_email=os.getenv('EMAIL_ACCOUNT'),receiver_email = email, subject='邮箱验证', content= email_content)
def send_email(smtp_server, sender_email, sender_password, receiver_email, subject, content):
    print('aaaaaaa1')
    # 创建一个SMTP客户端
    # client = smtplib.SMTP(smtp_server)
    client = smtplib.SMTP_SSL(smtp_server)
    print('aaaaaaa2')
    # 启动安全传输模式
    # client.starttls()
    print('aaaaaaa3')
    # 登录到你的邮箱
    client.login(sender_email, sender_password)
    print('aaaaaaa4')
    # 创建一封电子邮件
    msg = MIMEText(content, 'plain', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender_email
    msg['To'] = receiver_email

    # 发送电子邮件
    client.sendmail(sender_email, [receiver_email], msg.as_string())
    client.quit()


# ————————————————————————————————————————————笔记整理————————————————————————————————————————————————————
import pypandoc
import os
import time
def conver_markdow2pdf(markdown_file_path,pdf_file_path):
    output = pypandoc.convert_file(markdown_file_path,
                                   'pdf',
                                   outputfile=pdf_file_path,
                                   extra_args=[os.getenv('PDFLATEX_LOCATION')])
    assert output == "",'转换失败'

def delete_file_after_delay(file_path, delay):
    time.sleep(delay)
    if os.path.exists(file_path):
        os.remove(file_path)
    else:
        print("The file does not exist")


# ————————————————————————————————————————————对模型的访问————————————————————————————————————————————————————
import requests
import json
BASE_URL = os.getenv("MODEL_BASE_URL")
PROMPTS = {
    "chat": "你是一位否有经验的老师，现在请耐心回答以下学生的问题",
    "question": "以下是通过一款不可靠的文字识别软件识别出来的题目信息，请根据以下内容进行还原完整的题目信息后以json的格式进行返回。如果是问答题，json格式就是{question:\"question_content\"},如果是选择题，json格式就是{question:\"question_content\",options:[\"option1\",\"option2\",\"option3\",\"option4\"]}。以下是识别的问题的内容：",
    "note": "你是一位笔记制作大师，现在请根据以下内容整理笔记，并输出为markdown格式",
    "title": "根据以上内容生成即将产生发生的对话的标题，最好不超过10个字",
    "recommend": "请根据以下的题目信息进行题目的推荐，题目信息：",
}
# 0: chat, 1: question, 2: note
def pack_query(query,mode):
    return PROMPTS[mode]+query

def get_conversation_title(first_request):
    url = f"{BASE_URL}/v1/chat/completions"
    model_content = ['你是一位否有经验的老师，现在请耐心回答以下学生的问题']
    user_content = [first_request,PROMPTS['title']]
    data = {
        "model": "chatglm3-6b",
        "messages": [{"role": "user", "content": user_content}, {"role": "model", "content": model_content}]
    }
    response = requests.post(url, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']

def get_conversation_title_with_question(question_context,query):
    url = f"{BASE_URL}/v1/chat/completions"
    model_content = ['你是一位否有经验的老师，现在请耐心回答以下学生的问题',question_context['answer']]
    user_content = [question_context['question'],query,PROMPTS['title']]
    data = {
        "model": "chatglm3-6b",
        "messages": [{"role": "user", "content": user_content}, {"role": "model", "content": model_content}]
    }
    response = requests.post(url, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']


def get_response_for_chat(chat_context):
    url = f"{BASE_URL}/v1/chat/completions"
    data = {
        "model": "chatglm3-6b",
        "messages": [{"role": "user", "content": chat_context[::2]}, {"role": "model", "content": chat_context[1::2]}]
    }
    response = requests.post(url, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']


def get_question_from_raw_img_text(raw_img_text):
    url = f"{BASE_URL}/v1/embeddings"
    data = {
        "model": "chatglm3-6b",
        "messages": [{"role": "user", "content": raw_img_text}, {"role": "model", "content": PROMPTS['question']}]
    }
    response = requests.post(url, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']
def get_question_answer(question):
    url = f"{BASE_URL}/v1/chat/completions"
    data = {
        "model": "chatglm3-6b",
        "messages": [{"role": "user", "content": question}, {"role": "model", "content": PROMPTS['chat']}]
    }
    response = requests.post(url, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']
def note_orgainize(note_text):
    url = f"{BASE_URL}/v1/chat/completions"
    data = {
        "model": "chatglm3-6b",
        "messages": [{"role": "user", "content": note_text}, {"role": "model", "content": PROMPTS['note']}]
    }
    response = requests.post(url, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']

def get_recommended_questions(questions):
    url = f"{BASE_URL}/v1/chat/completions"
    data = {
        "model": "chatglm3-6b",
        "messages": [{"role": "user", "content": PROMPTS['recommend']+questions}]
    }
    response = requests.post(url, data=json.dumps(data))
    return response.json()['choices'][0]['message']['content']

