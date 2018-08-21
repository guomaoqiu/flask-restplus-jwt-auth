# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: user.py
# @Date:   2018-08-18 17:00:27
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-21 18:48:56
import logging
# from app.v1.roles import role_required
 #import role_required, api_doc_requerid
from flask import request,jsonify
from app import db
from app.v1.middleware import api_doc_required,role_required
from app.v1 import errors as error
from app.v1.conf.auth import refresh_jwt,auth
from app.v1.models.models import User, Blacklist
from app.v1.conf.auth import auth
from flask import g, url_for
from datetime import datetime
# from app.v1.schemas.schemas import UserSchema
from app.v1.mail.email import send_email
from app.v1 import v1_api
from flask_restplus import Resource, Namespace, fields
# from app.v1.fields.user_ns import register_model,login_model

user_ns = Namespace('user')
# {
#     "status": 0,
# Bearer eyJhbGciOiJIUzI1NiIsImV4cCI6MTUzNDg1MTgyMiwiaWF0IjoxNTM0ODQ4MjIyfQ.eyJhZG1pbiI6MCwiZW1haWwiOiJhZG1pbkBxcS5jb20ifQ.dXAGD84udSBB3zE8y_YW0OzyzGQ1iUl7xD8LoFCm5oU
#     "data": {
#         "username": "admin",
#         "user_id": 87,
#         "access_token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUzNDg1MTgyMiwiaWF0IjoxNTM0ODQ4MjIyfQ.eyJhZG1pbiI6MCwiZW1haWwiOiJhZG1pbkBxcS5jb20ifQ.dXAGD84udSBB3zE8y_YW0OzyzGQ1iUl7xD8LoFCm5oU",
#         "is_active": true,
#         "user_role": "user",
#         "refresh_token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUzNDg2NTQyMiwiaWF0IjoxNTM0ODQ4MjIyfQ.eyJlbWFpbCI6ImFkbWluQHFxLmNvbSJ9.vpuhSlo0kXSjeKFrakJS3PStvqEqLimEtwrqPu2EP2s"
#     },
#     "message:": "登录成功"
# parser settings
parser = user_ns.parser()
parser.add_argument('Authorization', type=str, \
					location='headers',help='Bearer Access Token',required=True)


@user_ns.route('/get_sa_data')
class get_sa_data(Resource):
    @user_ns.doc(parser=parser)
    @auth.login_required
    @role_required.permission(2)
    def get(self):
        return 'Sa data'

@user_ns.route('/get_admin_data')
class get_user_data(Resource):
    @user_ns.doc(parser=parser)
    @auth.login_required
    @role_required.permission(1)
    def get(self):
        return 'admin data'

@user_ns.route('/get_user_data')
class get_user_data(Resource):
	# 获取用户数据，这里需要header 需要携带上access_token才可以
    @user_ns.doc(parser=parser)
    @auth.login_required
    @role_required.permission(0)
    def get(self):
        return 'user data'


@user_ns.route('/delete_user')
class get_user_data(Resource):
    # 获取用户数据，这里需要header 需要携带上access_token才可以
    @user_ns.doc(parser=parser)
    @auth.login_required
    @user_ns.param('email',location='headers',required=True)
    def delete(self):
        return 'user data'                 