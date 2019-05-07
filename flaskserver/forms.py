# -*- coding: utf-8 -*-

from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField, ValidationError, HiddenField, \
    BooleanField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

from flaskserver.models import Admin


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')

class QueryForm(FlaskForm):
    kind = SelectField('分科', choices=((1, '理'), (2, '文'),))
    rank = IntegerField('排名', validators=[DataRequired()])
    grade = IntegerField('成绩', validators=[DataRequired()])
    submit = SubmitField('查询')

