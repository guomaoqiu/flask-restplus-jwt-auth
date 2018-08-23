# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: resources.py
# @Date:   2018-08-19 00:08:26
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-22 21:42:58

###### import module
import logging
from flask import request
from flask_restplus import Resource
from validate_email import validate_email
from app import db
from app.v1.model.user import User
from app.v1.extensions.auth.jwt_auth import refresh_jwt
from .serial import register_model, login_model, logout_model, rest_password_model,access_token_parser,auth_ns
from app.v1.utils.user_utils import  save_new_user
from app.v1.utils.auth_utils import  Auth



######  API
@auth_ns.route('/register')
class RegisterRquired(Resource):
    """注册接口"""
    @auth_ns.doc('user register')
    @auth_ns.expect(register_model, validate=True)
    def post(self):
        data = request.json
        return save_new_user(data=data)


@auth_ns.route('/login')
class LoginRquired(Resource):
    """登录接口"""
    @auth_ns.doc('user login',parser=access_token_parser)
    @auth_ns.expect(login_model, validate=True)
    def post(self):
        post_data = request.json
        return Auth.login_user(data=post_data)


@auth_ns.route('/logout')
class LoginRquired(Resource):
    """登录接口"""
    @auth_ns.doc('user logout')
    @auth_ns.expect(logout_model, validate=True)
    def post(self):
        post_data = request.json
        return Auth.logout(data=post_data)


####################
# ConfirmRquired
####################
@auth_ns.route('/confirm/<confirm_token>', endpoint="confirm")
class ConfirmRquired(Resource):
    """登录接口"""

    @auth_ns.doc('user email confirm')
    # @auth_ns.expect(login_model, validate=True)
    @auth_ns.param('email', required=True)
    def get(self, confirm_token):

        # Get Confirm email
        confirm_email = request.args.get('email')

        # Check confirm email
        if  validate_email(confirm_email, check_mx=True, verify=True):

            return {"message": "email invalid input."}, 423
        # use staticmethod verify confirm toke
        if User.verify_confirm_token(confirm_token, confirm_email):

            return {'message': 'User is active now'}, 200

        else:

            return {'message': 'User email confirmation failed, token may have expired, or email invalid'}, 202


####################
# RestPasswordRequired
####################
@auth_ns.route('/change_password')
class RestPasswordRequired(Resource):
    """重置密码"""
    @auth_ns.doc('rest password')
    # @auth_ns.doc(parser=parser)
    @auth_ns.expect(rest_password_model, validate=True)
    # @auth_ns.param('email',location='body',required=True)
    # @auth_ns.param('new_password',location='body',required=True)

    def put(self):
        pass


####################
# RestPasswordRequired
# ####################
#
# @auth_ns.route('/change_email')
# class RestPasswordRequired(Resource):
#     """更改邮箱"""
#
#     # @auth_ns.doc(parser=parser)
#     @auth_ns.expect(rest_password_model, validate=True)
#     # @auth_ns.param('email',location='body',required=True)
#     # @auth_ns.param('new_password',location='body',required=True)
#
#     def put(self):
#         pass


####################
# RefreshTokenRequired
####################

@auth_ns.route('/refresh_token')

class RefreshRequired(Resource):
    """登录接口"""
    @auth_ns.doc('refresh token')
    # @auth_ns.doc(parser=parser)
    @auth_ns.expect(rest_password_model, validate=True)
    # @auth_ns.param('email',location='body',required=True)
    # @auth_ns.param('new_password',location='body',required=True)

    def put(self):
        pass


