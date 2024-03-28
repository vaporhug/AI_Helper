from flask_sqlalchemy import SQLAlchemy
from flask_security import RoleMixin, UserMixin
from datetime import datetime

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

# class User(db.Model, UserMixin):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(100), unique=True)
#     email = db.Column(db.String(255), unique=True)
#     password = db.Column(db.String(255))
#     active = db.Column(db.Boolean())
#     fs_uniquifier = db.Column(db.String(64), unique=True)  # For Flask-Security
#     gender = db.Column(db.String(10))  # Assuming 'male', 'female', 'other'
#     age = db.Column(db.Integer)
#     status = db.Column(db.String(50))  # 'college_student', 'high_school_student', 'employed'
#     questions = db.relationship('Question', backref='user', lazy='dynamic')
#
# class Question(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
#     category = db.Column(db.String(100))
#     content = db.Column(db.Text)
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
