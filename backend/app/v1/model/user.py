# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: user.py
# @Date:   2018-08-18 18:03:19
# @Last Modified by:   Green
# @Last Modified time: 2018-10-15 15:32:16

import logging
from app import db
from app.v1.extensions.auth.jwt_auth import jwt, auth, confirm_email_jwt
from flask import g, request, jsonify
import hashlib
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context


class User(db.Model):
    # Generates default class name for table. For changing use
    #__tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    public_id = db.Column(db.String(100), unique=True)
    username = db.Column(db.String(64))
    user_role = db.Column(db.String(length=30), default='user')
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean, default=False)
    mobile = db.Column(db.String(11))
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.now)
    last_seen = db.Column(db.DateTime(), default=datetime.now)
    avatar_hash = db.Column(db.String(32))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    # Hash the register user password
    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    # Check password
    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    # Generates auth token.
    def generate_auth_token(self, permission_level):
        """生成token"""
        # Check if admin.
        if permission_level == 1:

            # Generate admin token with flag 1.
            token = jwt.dumps({'email': self.email, 'admin': 1}).decode('ascii')


            # Return admin flag.
            return token

            # Check if admin.
        elif permission_level == 2:

            # Generate admin token with flag 2.
            token = jwt.dumps({'email': self.email, 'admin': 2}).decode('ascii')

            # Return admin flag.
            return token

        # Return normal user flag permission_level == 0 .
        # python 2 dumps过后是str, 而在python3 中dumps的结果为bytes,
        # 则需要将bytes转为字符串，即可 decode('ascii)
        # 否则会报错: "TypeError: Object of type 'bytes' is not JSON serializable"

        #print(jwt.make_header(header_fields={'token': jwt.dumps({'email': self.email, 'admin': 0}).decode('ascii')}))
        token = jwt.dumps({'email': self.email, 'admin': 0}).decode('ascii')
        #jwt.make_header(header_fields=token)
        return token


    # Generates a new access token from refresh token.
    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):
        """验证token"""
        # Create a global none user.
        g.user = None

        try:
            # Load token.
            data = jwt.loads(token)

        except Exception as why:
            logging.error(why)
            # If any error return false.
            return False

        # Check if email and admin permission variables are in jwt.
        if 'email' and 'admin' in data:
            # Set email from jwt.
            g.user = data['email']

            # Set admin permission from jwt.
            g.admin = data['admin']

            # Return true.
            return True
        # If does not verified, return false.

        return False

    #Generates confirmation token.
    def generate_confirmation_token(self, email, username):

       return confirm_email_jwt.dumps({'email': self.email, 'username': self.username}).decode('ascii')

    # Check token
    @staticmethod
    def verify_confirm_token(confirm_token, confirm_email):
        try:

            data = confirm_email_jwt.loads(confirm_token)
            print (('s',confirm_email))
            # if token is exp,return None
            if confirm_email == data['email']:
                user = User.query.filter_by(email=data['email']).first()

                # set is_activce is 1
                user.is_active = 1
                #print(user)
                db.session.add(user)
                db.session.commit()

                return True

        except Exception as why:
            logging.info("User email confirmation failed, token may have expired " + str(why))
            print ("token exp.....")
            return None
        else:
            return False

    # Get reset token
    def generate_reset_token(self):

        return jwt.dumps({'reset': self.id}).decode('ascii')


    # Change password
    def reset_password(self, token, new_password):

        try:
            data = jwt.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        return True

    # Get reset change token
    def generate_email_change_token(self, new_email):
        return jwt.dumps({'change_email': self.id, 'new_email': new_email})

    # 用户头像
    def gravatar(self, size=100, default='identicon', rating='g'):

        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        data = '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)
        return data

    # Change email
    def change_email(self, token):
        # 更改邮箱
        try:
            data = jwt.loads(token)
        except:
            return False
        if data.get('change_email') != self.id:
            return False
        new_email = data.get('new_email')
        if new_email is None:
            return False
        if self.query.filter_by(email=new_email).first() is not None:
            return False
        self.email = new_email
        db.session.add(self)
        return True

    def __repr__(self):

        # This is only for representation how you want to see user information after query.
        return "<User(id='%s', username='%s',email='%s')>" % (self.id, self.username, self.email)
    #
    # # 类方法 class_method
    # @classmethod
    # def return_all(cls):
    #     def to_json(self):
    #         return {
    #             'id': self.id,
    #             'email': self.email,
    #             'mobile': self.mobile,
    #             'username': self.username,
    #             'user_role': self.user_role,
    #             'is_active': self.is_active,
    #             'name': self.name,
    #             'member_since': str(self.member_since),
    #         }
    #
    #     return {'users': list(map(lambda x: to_json(x), User.query.all()))}
    #
    # @classmethod
    # def delete_all(cls):
    #     try:
    #         num_rows_deleted = db.session.query(cls).delete()
    #         db.session.commit()
    #         return {'status': 0, 'message': '{} row(s) deleted'.format(num_rows_deleted)}
    #     except:
    #         return {'status': 1, 'message': 'Something went wrong'}
    #

