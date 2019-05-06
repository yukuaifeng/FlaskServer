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
    kind = SelectField('Kind', coerce=int, default=1)
    rank = IntegerField('Rank', validators=[DataRequired(), Length(1, 10)])
    grade = IntegerField('Grade', validators=[DataRequired(), Length(1, 4)])
    submit = SubmitField('query')

