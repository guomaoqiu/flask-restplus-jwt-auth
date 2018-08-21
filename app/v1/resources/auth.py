# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: auth.py
# @Date:   2018-08-19 00:08:26
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-21 14:24:48


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
from app.v1.middleware import api_doc_required,role_required
from flask_restplus import Resource, Namespace, fields, reqparse
from app.v1.fields.auth_ns import register_model,login_model
from validate_email import validate_email

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class RegisterAPI(Resource):
    """注册接口"""
    # @auth_ns.doc(parser=register_parser)
    @auth_ns.expect(register_model, validate=True)
    def post(self):
        try:
            # Get username, password and email.
            reg_username, reg_password, reg_email = request.json.get('username').strip(), request.json.get('password').strip(), \
                                        request.json.get('email').strip()
            print reg_username,reg_password,reg_email
     
        except Exception as why:

            # Log input strip or etc. errors.
            logging.info("Username, password or email is wrong. " + str(why))

            # Return invalid input error.
            return {"message" : "invalid input.5555"}, 422

        # Check if any field is none.
        if reg_username is None or reg_password is None or reg_email is None:

            return {"message" : "invalid inputxcccccc."}, 422

        if not validate_email(reg_email):
            return {"message" : "email invalid input."}, 423
    
        # Get user if it is existed.
        user = User.query.filter_by(email=reg_email,username=reg_username).first()

        # Check if user is existed.
        if user is not None:
           return {"message" : "user already exist."}, 922
        
        # Create a new user.
        user = User(username=reg_username, password_hash=reg_password, email=reg_email)

        # Hash register password
        # user.hash_password(reg_password)

        # # Add user to session.
        # db.session.add(user)
        # # Commit session.
        # db.session.commit()

        # Return success if registration is completed.
        confirm_token = user.generate_confirmation_token(user.email,user.username)
        
        #print ("%s Confirm_token is: %s" % (user.username,confirm_token + "?email="+user.email))
        # build confirm url
        print url_for("confirm",confirm_token=confirm_token)

        #send_email(user.email, 'Confirm Email', 'email_tpl/confirm', user=user, token=token, confirm_url=confirm_url)

        return {
                'status': 0,
                'message': "注册成功，请检查邮件进行确认.",
                    'data': {
                        'user_id': user.id,
                        'username': reg_username,
                        'create_time': str(user.member_since)
                    }
                
                }

@auth_ns.route('/login')
class LoginAPI(Resource):
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
            return {"message" : "invalid input."}, 422

        # Check if user information is none.
        if email is None or password is None:

            return {"message" : "invalid input."}, 422

        # Get user if it is existed.
        user = User.query.filter_by(email=email).first()

        # Check if user is not existed.
        if user is None:
            return {"message" : "does not exist."}, 404

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
                return  {"message" : "invalid input."}, 422

            # 根据用户登录邮箱生成refresh_token.
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
            # 返回无效密码提示
            return  {"message" : "invalid pasword."}, 421      



@auth_ns.route('/confirm/<confirm_token>',endpoint="confirm")
class Confirm(Resource):
    """登录接口"""
    # @auth_ns.expect(login_model, validate=True)
    @auth_ns.param('email',required=True)

    def get(self,confirm_token):

        confirm_email=request.args.get('email')
        user = User()
        if user.verify_confirm_token(confirm_token,confirm_email):
            return {'message':'User is active now'}, 200
        else: 
            return {'message':'User email confirm faild.'}, 202
