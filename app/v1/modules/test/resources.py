# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: user.py
# @Date:   2018-08-18 17:00:27
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-21 23:05:38

import logging
# from app.v1.roles import role_required
# import role_required, api_doc_requerid
from flask import request, jsonify
from app import db
from app.v1.middleware import api_doc_required, role_required
from app.v1 import errors as error
from app.v1.extensions.auth.jwt_auth import refresh_jwt, auth
from flask_restplus import Resource, Namespace, fields


test_ns = Namespace('test')

@test_ns.route('/get_user_data')
class get_user_data(Resource):
    @auth.login_required
    @role_required.permission(0)
    def get(self):
        return "user data"

@test_ns.route('/get_admin_data')
class get_admin_data(Resource):
    @auth.login_required
    @role_required.permission(1)
    def get(self):
        return "admin data"

@test_ns.route('/get_sa_data')
class get_admin_data(Resource):
    @auth.login_required
    @role_required.permission(2)
    def get(self):
        return "sa data"