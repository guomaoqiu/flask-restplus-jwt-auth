# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: config.py
# @Date:   2018-08-18 16:55:23
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-21 15:06:06

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
    MAIL_PASSWORD =  ''
    FLASKY_MAIL_SUBJECT_PREFIX = u'[XXOO]'
    FLASKY_MAIL_SENDER = '2399447849@qq.com'
    FLASKY_ADMIN = '2399447849@qq.com'
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = False
    db_host = 'localhost'
    db_user = 'root'
    db_pass = '123.com'
    db_name = 'restapi'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://' + db_user + ':' + db_pass + '@' + db_host + '/' + db_name
    SQLALCHEMY_ECHO=False
    SQLALCHEMY_TRACK_MODIFICATIONS=True

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'

class Production(Config):
 
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': Production,
    'default': DevelopmentConfig
}

