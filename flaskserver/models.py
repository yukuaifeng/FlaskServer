# -*- coding: utf-8 -*-

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from flaskserver.extensions import db

#用户信息表
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        print(self.password_hash.split('$', 2))
        print("uzko90aC$dc6d27fb85d0a1b46b16e597d70733820dba90d824e4844550c1806f974bcb3a")
        return check_password_hash(self.password_hash, password)
        # check = False
        # if (password == self.password_hash):
        #     check = True
        # return check

    def validate_username(self, username):
        if User.query.filter_by(username=username).first():
            return False

#院校录取名次表
class Admission(db.Model):
    __tablename__ = 'grade_line'
    id = db.Column(db.Integer, primary_key=True)
    school = db.Column(db.String(50))
    rank = db.Column(db.Integer)
    year = db.Column(db.Integer) #Integer 不能像String一样加入后面的数字标志
    kind = db.Column(db.String(4))
    grade = db.Column(db.Integer)
    clazz = db.Column(db.String(8))

#新的所有数据的表格
class GradeLine(db.Model):
    __tablename__ = 'grade_all'
    id = db.Column(db.Integer, primary_key=True)
    kind = db.Column(db.String(10))
    number = db.Column(db.Integer)
    school = db.Column(db.String(50))
    figure = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    chinese = db.Column(db.Float)
    math = db.Column(db.Float)
    english = db.Column(db.Float)
    year = db.Column(db.Integer)
    rank = db.Column(db.Integer)
    clazz = db.Column(db.String(10))

#历年高考省控线及其排名
class ControlLine(db.Model):
    __tablename__ = 'control_line'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    kind = db.Column(db.String(10))
    clazz = db.Column(db.String(10))
    ctrl_line = db.Column(db.Integer)
    ctrl_rank = db.Column(db.Integer)

#历年参加高考人数表
class StudentNumber(db.Model):
    __tablename__ = 'student_number'
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer)
    stu_num = db.Column(db.Integer)

