from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin

from sqlalchemy import JSON

db = SQLAlchemy()

roles_users = db.Table('roles_users',
        db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
        db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    gender = db.Column(db.String(10))
    age = db.Column(db.Integer)
    role = db.Column(db.String(20))
    password = db.Column(db.String(255))
    conversation_histories = db.relationship('ConversationHistory', backref='user',
                                lazy='dynamic')

# 题目表
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    category = db.Column(db.String(50))
    content = db.Column(db.Text)

# 用户与题目之间的关系表
class UserQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))

    user = db.relationship('User', backref=db.backref('user_questions', lazy='dynamic'))
    question = db.relationship('Question', backref=db.backref('user_questions', lazy='dynamic'))

class ConversationHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), index=True)
    title = db.Column(db.String(120), nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False)
    content = db.Column(JSON, nullable=False)
