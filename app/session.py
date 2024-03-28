from flask import Flask, request, jsonify
import redis



class SessionStore:
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
        SessionStore.__redis_connection = redis.Redis(host=host, port=port, db=db)

    @staticmethod
    def get_redis_connection():
        """
        获取存储的 Redis 连接。

        返回:
        返回 Redis 连接实例
        """
        if SessionStore.__redis_connection is None:
            raise Exception("Redis connection is not initialized. Please call 'initialize_connection' first.")
        return SessionStore.__redis_connection

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
        redis_connection = SessionStore.get_redis_connection()
        redis_connection.rpush(f'session:{session_id}:requests', user_request)
        redis_connection.rpush(f'session:{session_id}:responses', server_response)

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
        redis_connection = SessionStore.get_redis_connection()
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
        redis_connection = SessionStore.get_redis_connection()
        redis_connection.delete(f'session:{session_id}:requests')
        redis_connection.delete(f'session:{session_id}:responses')

