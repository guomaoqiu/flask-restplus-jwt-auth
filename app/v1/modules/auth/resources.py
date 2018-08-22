# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: auth.py
# @Date:   2018-08-19 00:08:26
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-22 01:05:44


import logging
from flask import request
from app import db
from app.v1.extensions.auth.jwt_auth import refresh_jwt, auth
from .models import User, Blacklist
from flask import g, url_for
from app.v1.mail.email import send_email
from flask_restplus import Resource, Namespace
from .parameters import register_model, login_model, rest_password_model
from validate_email import validate_email

auth_ns = Namespace('auth')

parser = auth_ns.parser()
parser.add_argument('Authorization',
                    type=str,
                    required=True,
                    location='headers',
                    help='Bearer Access Token')


####################
# RegisterAPI
####################
@auth_ns.route('/register')
class RegisterRquired(Resource):
    """注册接口"""
    @auth_ns.expect(register_model, validate=True)
    def post(self):
        try:
            # Get username, password and email.
            reg_username, reg_password, reg_email = request.json.get('username').strip(), \
                                                    request.json.get('password').strip(), \
                                                    request.json.get('email').strip()

        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Username, password or email is wrong. " + str(why))

            # Return invalid input error.
            return {"message": "invalid input.5555"}, 422

        # Check if any field is none.
        if reg_username is None or reg_password is None or reg_email is None:
            return {"message": "invalid input."}, 422

        # Check email address
        if not validate_email(reg_email, check_mx=True, verify=True):
            return {"message": "email invalid input."}, 423

        # Get user if it is existed.
        user = User.query.filter_by(email=reg_email).first()

        # Check if user is existed.
        if user is not None:
            return {"message": "user already exist."}, 922

        # Create a new user.
        user = User(username=reg_username, password_hash=reg_password, email=reg_email)

        # Hash register password
        user.hash_password(reg_password)

        # Add user to session.
        db.session.add(user)
        # Commit session.
        db.session.commit()

        # Return success if registration is completed.
        confirm_token = user.generate_confirmation_token(user.email, user.username)

        # Generation email confirm url
        confirm_url = url_for("v1_blueprint.confirm",
                              confirm_token=confirm_token,
                              _external=True) + "?email=" + user.email

        print (confirm_url)

        send_email(user.email, 'Confirm Email', 'email_tpl/confirm',
                   user=user.username,
                   token=confirm_token,
                   confirm_url=confirm_url)

        return {
            'status': 0,
            'message': "注册成功，请检查邮件进行确认.",
            'data': {
                'user_id': user.id,
                'username': reg_username,
                'create_time': str(user.member_since)
            }
        }


####################
# LoginAPI
####################
@auth_ns.route('/login')
class LoginRquired(Resource):
    """登录接口"""

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

        # 如果密码认证通过，则通过登录用户角色生成access_token
        # 这里分了三种角色(用户注册时就已经分配好了默认角色user)
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

            # 根据用户登录邮箱生成refresh_token.
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
            # 返回无效密码提示
            return {"message": "invalid pasword."}, 421


            ####################


# ConfirmRquired
####################
@auth_ns.route('/confirm/<confirm_token>', endpoint="confirm")
class ConfirmRquired(Resource):
    """登录接口"""

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
    """登录接口"""

    # @auth_ns.doc(parser=parser)
    @auth_ns.expect(rest_password_model, validate=True)
    # @auth_ns.param('email',location='body',required=True)
    # @auth_ns.param('new_password',location='body',required=True)

    def put(self):
        pass


####################
# RestPasswordRequired
####################

@auth_ns.route('/change_email')
class RestPasswordRequired(Resource):
    """登录接口"""

    # @auth_ns.doc(parser=parser)
    @auth_ns.expect(rest_password_model, validate=True)
    # @auth_ns.param('email',location='body',required=True)
    # @auth_ns.param('new_password',location='body',required=True)

    def put(self):
        pass


####################
# RefreshTokenRequired
####################

@auth_ns.route('/refresh_token')

class RefreshRequired(Resource):
    """登录接口"""

    # @auth_ns.doc(parser=parser)
    @auth_ns.expect(rest_password_model, validate=True)
    # @auth_ns.param('email',location='body',required=True)
    # @auth_ns.param('new_password',location='body',required=True)

    def put(self):
        pass


# from app.v1.errors import CustomFlaskErr
from app.v1 import errors


@auth_ns.route('/test')
class Restest(Resource):
    """docstring for test"""

    def get(self):
        return 'o'
