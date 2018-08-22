# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: parameters.py
# @Date:   2018-08-18 21:41:37
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-22 21:26:34
from app.v1 import v1_api

from flask_restplus import fields, reqparse


user_put_model = v1_api.model('DeleterUserRequired', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
})


get_user_fields = v1_api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'user_role': fields.String(required=True, description='user user_role'),
        'is_active': fields.String(required=True, description='user is_active'),
        'mobile': fields.String(required=True, description='user mobile'),
        'about_me': fields.String(required=True, description='user info'),
        'member_since': fields.String(required=True, description='user register time'),
})

