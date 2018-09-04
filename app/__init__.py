# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: __init__.py
# @Date:   2018-08-18 23:28:31
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-24 00:03:37

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(config[config_name])
    app.app_context().push()

    db.init_app(app)
    db.create_all()

    # 注册到Flask 核心对象
    from .v1 import v1_blueprint
    app.register_blueprint(v1_blueprint, url_prefix='/api/v1')

    # Swagger ui config
    app.config.SWAGGER_UI_OPERATION_ID = True
    app.config.SWAGGER_UI_REQUEST_DURATION = True
    # You can also specify the initial expansion state with \
    # the config.SWAGGER_UI_DOC_EXPANSION setting ('none', 'list' or 'full'):
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

    return app
