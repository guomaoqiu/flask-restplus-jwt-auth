# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: resources.py
# @Date:   2018-08-19 00:08:26
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-22 21:42:58

import logging

from flask import request
from flask_restplus import Resource, Namespace
from validate_email import validate_email
from app import db
from app.v1.database.models import User
from app.v1.extensions.auth.jwt_auth import refresh_jwt
from .parameters import register_model, login_model, rest_password_model
from app.v1.utils.user_utils import  save_new_user

auth_ns = Namespace('auth')

parser = auth_ns.parser()
parser.add_argument('Authorization',
                    type=str,
                    required=True,
                    location='headers',
                    help='Bearer Access Token')


@auth_ns.route('/register')
class RegisterRquired(Resource):
    """注册接口"""
    @auth_ns.doc('user register')
    @auth_ns.expect(register_model, validate=True)
    def post(self):
        data = request.json
        return save_new_user(data=data)


####################
# LoginAPI
####################
@auth_ns.route('/login')
class LoginRquired(Resource):
    """登录接口"""
    @auth_ns.doc('user login')
    @auth_ns.expect(login_model, validate=True)
    def post(self):

        try:
            # Get user email and password.
            email, password = request.json.get('email').strip(), request.json.get('password').strip()

        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Email or password is wrong. " + str(why))

            # Return invalid input error.
            return {"message": "invalid input."}, 422

        # Check if user information is none.
        if email is None or password is None:
            return {"message": "invalid input."}, 422

        # Get user if it is existed.
        user = User.query.filter_by(email=email).first()
        # Check if user is not existed.
        if user is None:
            return {"message": "does not exist."}, 404

        if not user.is_active:
            return {'message': 'user not activated.'}, 988

        # Generate an access token if the password is correct.
        # Three roles for user, default user role is user.
        # user：0，admin:1, sa:2
        if user is not None and user.verify_password(password):

            if user.user_role == 'user':

                # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
                access_token = user.generate_auth_token(0)

            # If user is admin.
            elif user.user_role == 'admin':

                # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
                access_token = user.generate_auth_token(1)

            # If user is super admin.
            elif user.user_role == 'sa':

                # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 2, 1, 0.
                access_token = user.generate_auth_token(2)

            else:
                return {"message": "invalid input."}, 422

            # Generate refresh_token based on the user emamil.
            refresh_token = (refresh_jwt.dumps({'email': email})).decode('ascii')

            # Commit session.
            db.session.commit()

            return {
                'status': 0,
                'message:': 'Login Success',
                'data': {
                    'user_id': user.id,
                    'is_active': user.is_active,
                    'username': user.username,
                    'user_role': user.user_role,
                    'access_token': access_token,
                    'refresh_token': refresh_token
                }
            }
        else:
            # Return invalid password
            return {"message": "invalid pasword."}, 421


            

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


