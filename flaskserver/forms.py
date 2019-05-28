# -*- coding: utf-8 -*-


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField,  HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, ValidationError, Regexp, EqualTo
from wtforms import ValidationError

from flaskserver.models import User


def check_num(form, field):
    if field.data > 10:
        raise ValidationError('数目不得大于10')

def check_rank(form, field):
    if field.data > 99629:
        raise ValidationError('暂时不支持大于99629名之后的查询')

#查询用表格
class QueryForm(FlaskForm):
    kind = SelectField('分科', choices=((1, '理科'), (2, '文科'),))
    rank = IntegerField('排名', validators=[DataRequired('不能为空'), check_rank])
    grade = IntegerField('成绩', validators=[DataRequired('不能为空')])
    risk_num = IntegerField('冲的数目', validators=[check_num])
    sure_num = IntegerField('稳的数目', validators=[check_num])
    def_num = IntegerField('保的数目', validators=[check_num])
    submit = SubmitField('查询')

    def validate_rank(form, field):
        if field.data > 99629:
            raise ValidationError('暂时不支持99629名之后的查询')

#登录用的表格
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    verify_code = StringField('VerifyCode', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


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


