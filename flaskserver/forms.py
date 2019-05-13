# -*- coding: utf-8 -*-

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, ValidationError, HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, Regexp, EqualTo
from wtforms import ValidationError

from flaskserver.models import User

#登录用的表格
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    verify_code = StringField('VerifyCode', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

#查询用表格
class QueryForm(FlaskForm):
    kind = SelectField('分科', choices=((1, '理科'), (2, '文科'),))
    rank = IntegerField('排名', validators=[DataRequired()])
    grade = IntegerField('成绩', validators=[DataRequired()])
    submit = SubmitField('查询')

#注册用表格
class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20),
                            Regexp('^[a-zA-Z0-9]*$', message='The username should contain only a-z,A-Z and 0-9 ')])
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('Confirm password', validators=[DataRequired(), Length(8, 128)])
    verify_code = StringField('VerifyCode', validators=[DataRequired()])
    submit = SubmitField()

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('The email is already in use.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('The username is already in use.')


