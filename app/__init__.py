# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: __init__.py
# @Date:   2018-08-18 23:28:31
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-21 14:53:32

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app(config_name):
    from config import config
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from .v1 import v1_blueprint
    app.register_blueprint(v1_blueprint, url_prefix='/restapi/v1')

    from app.v1.resources import auth
    app.register_blueprint(auth, url_prefix='/auth')
    
    app.config.SWAGGER_UI_OPERATION_ID = True
    app.config.SWAGGER_UI_REQUEST_DURATION = True
    # You can also specify the initial expansion state with \
    # the config.SWAGGER_UI_DOC_EXPANSION setting ('none', 'list' or 'full'):
    # app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    app.config.SWAGGER_VALIDATOR_URL = 'http://domain.com/validator'


    return app
