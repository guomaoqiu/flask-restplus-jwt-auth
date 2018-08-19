# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: __init__.py
# @Date:   2018-08-18 23:28:31
# @Last Modified by:   Green
# @Last Modified time: 2018-08-19 00:23:27
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_type='dev'):
    from config import config
    app = Flask(__name__)
    app.config.from_object(config[config_type])

    db.init_app(app)

    from .v1 import v1_blueprint
    app.register_blueprint(v1_blueprint, url_prefix='/restapi/v1')
    app.config.SWAGGER_UI_OPERATION_ID = True
    app.config.SWAGGER_UI_REQUEST_DURATION = True
    # You can also specify the initial expansion state with \
    # the config.SWAGGER_UI_DOC_EXPANSION setting ('none', 'list' or 'full'):
    # app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    app.config.SWAGGER_VALIDATOR_URL = 'http://domain.com/validator'


    return app
