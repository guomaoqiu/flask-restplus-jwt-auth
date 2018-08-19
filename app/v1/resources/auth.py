# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: auth.py
# @Date:   2018-08-19 00:08:26
# @Last Modified by:   Green
# @Last Modified time: 2018-08-19 12:19:15


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
from app.v1.fields.auth_ns import register_model,login_model


auth_ns = Namespace('auth')


@auth_ns.route('/register')
class Register(Resource):
    @auth_ns.expect(register_model, validate=True)
   
    @auth_ns.response(405, 'userndsdrd incorrect')

    def post(self):
        try:
            # Get username, password and email.
            username, password, email = request.json.get('username').strip(), request.json.get('password').strip(), \
                                        request.json.get('email').strip()
        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Username, password or email is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if any field is none.
        if username is None or password is None or email is None:
            return error.INVALID_INPUT_422

        # Get user if it is existed.
        user = User.query.filter_by(email=email,username=username).first()

        # Check if user is existed.
        if user is not None:
           return error.ALREADY_EXIST

        # Create a new user.
        user = User(username=username, password_hash=password, email=email)
        user.hash_password(password)

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Return success if registration is completed.
        token = user.generate_confirmation_token()

        # build confirm url
        #confirm_url = url_for('confirm', token=token, _external=True) + "?email=" + user.email
        #print confirm_url

        #send_email(user.email, 'Confirm Email', 'email_tpl/confirm', user=user, token=token, confirm_url=confirm_url)

        return {
                'status': 0,
                'message': "注册成功，请检查邮件进行确认.",
                    'data': {
                        'user_id': user.id,
                        'username': username,
                        'create_time': str(user.member_since)
                    }
                
                }

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model, validate=True)
    @auth_ns.param(paramType="header", name="fdsfsd")

    def post(self):

        try:
            # Get user email and password.
            email, password = request.json.get('email').strip(), request.json.get('password').strip()

        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Email or password is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        # Check if user information is none.
        if email is None or password is None:

            return error.INVALID_INPUT_422

        # Get user if it is existed.
        user = User.query.filter_by(email=email).first()

        # Check if user is not existed.
        if user is None:

            return error.DOES_NOT_EXIST

        if not user.is_active:
            return {
                'status': 1,
                'message': '用户未激活.'
                }

        # Check passowrd    
        if user is not None and user.verify_password(password):
        
            if user.user_role == 'user':

                # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
                access_token = user.generate_auth_token(0)
                print access_token
                print user.username

            # If user is admin.
            elif user.user_role == 'admin':

                # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
                access_token = user.generate_auth_token(1)

            # If user is super admin.
            elif user.user_role == 'sa':

                # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 2, 1, 0.
                access_token = user.generate_auth_token(2)

            else:
                return error.INVALID_INPUT_422

            # Generate refresh token.
            refresh_token = refresh_jwt.dumps({'email': email})

            # Commit session.
            db.session.commit()


            return {
                    'status': 0,
                    'message:': '登录成功',
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
            # return invalid passowrd
            return error.PASSWORD_INVALID_421      

@auth_ns.route('/get_user_data')
class DataUserRequired(Resource):

    @auth_ns.doc(security='apiKey')
    # @api_doc_required.permission
    @auth.login_required
    @role_required.permission(0)
    def get(self):

        return 'ok'
