# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: config.py
# @Date:   2018-08-18 16:55:23
# @Last Modified by:   Green
# @Last Modified time: 2018-08-19 00:23:33

import os

class Config:
    """basic config"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A0Zr98j/3yXR~XHH!jmN]LWX/,?RT'
    #SSL_DISABLE = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True

    # send mail
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = '2399447849'
    MAIL_PASSWORD =  'guomaoqiu.150019'
    FLASKY_MAIL_SUBJECT_PREFIX = u'[XXOO]'
    FLASKY_MAIL_SENDER = '2399447849@qq.com'
    FLASKY_ADMIN = '2399447849@qq.com' # os.environ.get('FANXIANG_ADMIN')
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = False
    db_host = 'localhost'
    db_user = 'root'
    db_pass = '123.com'
    db_name = 'restapi'
    SQLALCHEMY_DATABASE_URI = 'mysql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name
    SQLALCHEMY_ECHO=False

    SQLALCHEMY_TRACK_MODIFICATIONS=True
    #RECAPTCHA_PUBLIC_KEY = '6LdCijkUAAAAAKo5KAdTE7XR7yA_PRvLHgmVlGeW'
    #RECAPTCHA_PRIVATE_KEY = '6LdCijkUAAAAAJTB0xosM4D_YTJmN3gxRmuJ-Jfj'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'mysql://flask:flask@127.0.0.1/flask-test'
    WTF_CSRF_ENABLED = False

class Production(Config):
    DEBUG = True
    db_host = 'db'
    db_user = 'flask'
    db_pass = 'local_ops'
    db_name = 'local_ops'
    SQLALCHEMY_DATABASE_URI = 'mysql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name
    SQLALCHEMY_ECHO=False #用于显式地禁用或启用查询记录

    ##SQLALCHEMY_DATABASE_URI = 'mysql://flask1:flask1@127.0.0.1/flask1'
    SQLALCHEMY_TRACK_MODIFICATIONS=True
    #google 验证码
    #RECAPTCHA_PUBLIC_KEY = '6LdCijkUAAAAAKo5KAdTE7XR7yA_PRvLHgmVlGeW'
    #RECAPTCHA_PRIVATE_KEY = '6LdCijkUAAAAAJTB0xosM4D_YTJmN3gxRmuJ-Jfj'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Production,
    'default': DevelopmentConfig
}

