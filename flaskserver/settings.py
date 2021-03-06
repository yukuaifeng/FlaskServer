# -*- coding: utf-8 -*-

import os
import sys
import pymysql

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
baseurl = "mysql+pymysql://root:950305@127.0.0.1:3306/evolution"

# SQLite URI compatible
WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'


class BaseConfig(object):
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')

    DEBUG_TB_INTERCEPT_REDIRECTS = False

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True

    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    MAIL_SERVER = 'smtp.sendgrid.net'
    MAIL_PORT = 587
    #MAIL_USE_SSL = True
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'apikey'
    MAIL_PASSWORD = os.getenv('SENDGRID_API_KEY')
    MAIL_DEFAULT_SENDER = ('yukuaifeng', os.getenv('MAIL_PASSWORD'))
    SECURITY_EMAIL_SENDER = 'valid_email@my_domain.com'
    #
    # BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
    # BLUELOG_POST_PER_PAGE = 10
    # BLUELOG_MANAGE_POST_PER_PAGE = 15
    # BLUELOG_COMMENT_PER_PAGE = 15
    # # ('theme name', 'display name')
    # BLUELOG_THEMES = {'perfect_blue': 'Perfect Blue', 'black_swan': 'Black Swan'}
    # BLUELOG_SLOW_QUERY_THRESHOLD = 1
    #
    # BLUELOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    # BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


class DevelopmentConfig(BaseConfig):
    #SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')
    SQLALCHEMY_DATABASE_URI = baseurl


class TestingConfig(BaseConfig):
    TESTING = True
    WTF_CSRF_ENABLED = False
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database
    SQLALCHEMY_DATABASE_URI = baseurl


class ProductionConfig(BaseConfig):
    #SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))
    SQLALCHEMY_DATABASE_URI = baseurl


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

class Operations:
    CONFIRM = 'confirm'
    RESET_PASSWORD = 'reset-password'
    CHANGE_EMAIL = 'change-email'