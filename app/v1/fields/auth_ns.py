# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: auth_ns.py
# @Date:   2018-08-18 21:41:37
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-21 12:16:38
from app.v1 import v1_api

from flask_restplus import fields, reqparse

register_model = v1_api.model('Register', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
})

login_model = v1_api.model('Login', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
})



