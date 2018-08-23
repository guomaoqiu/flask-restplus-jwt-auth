# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: serial.py
# @Date:   2018-08-18 21:41:37
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-24 00:06:51
from app.v1 import v1_api

from flask_restplus import fields,Namespace


register_model = v1_api.model('Register', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
})

login_model = v1_api.model('Login', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
})

logout_model = v1_api.model('Logout', {
        'refresh_token': fields.String(required=True, description='refresh token'),
})

refresh_token_model = v1_api.model('RefeshToken', {
        'refresh_token': fields.String(required=True, description='refresh token'),
})

rest_password_model = v1_api.model('RestPassword', {
        'email': fields.String(required=True, description='user email address'),
        'old_password': fields.String(required=True, description='user old password'),
        'new_password': fields.String(required=True, description='user new password'),
})


