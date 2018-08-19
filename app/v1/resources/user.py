# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: user.py
# @Date:   2018-08-18 17:00:27
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-19 17:56:59
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


# parser settings
parser = user_ns.parser()
parser.add_argument('Authorization', type=str, \
					location='headers',help='Access Token',required=True)


@user_ns.route('/get_sa_data')
class get_sa_data(Resource):
    @user_ns.doc(security='apiKey',parser=parser)
    @auth.login_required
    @role_required.permission(2)
    def get(self):
        return 'Sa data'

@user_ns.route('/get_admin_data')
class get_user_data(Resource):
    @user_ns.doc(security='apiKey',parser=parser)
    @auth.login_required
    @role_required.permission(1)
    def get(self):
        return 'admin data'

@user_ns.route('/get_user_data')
class get_user_data(Resource):
	# 获取用户数据，这里需要header 需要携带上access_token才可以
    @user_ns.doc(security='apiKey',parser=parser)
    @auth.login_required
    @role_required.permission(0)
    def get(self):
        return 'user data'