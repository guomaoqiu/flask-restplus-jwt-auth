# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: user_utils.py
# @Date:   2018-08-23 11:03:15
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-23 22:47:46
import datetime
import uuid
from flask import url_for
from app import db
from app.v1.model.user import User
import hashlib
from datetime import datetime
from passlib.apps import custom_app_context as pwd_context
from validate_email import validate_email
from app.v1.mail import email

def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()

    if not validate_email(data['email'],verify=True,check_mx=True):
       return {'message':'invalid email'}

    if not user :
        user = User(
            public_id=str(uuid.uuid4()),
            email=data['email'],
            username=data['username'],
            password_hash=data['password']
        )
        # Hash new user password
        user.hash_password(data['password'])

        save_changes(user)

        response_object={  'status': 0,
            'message': "Registration is successful, please check the email to confirm.",
            'data': {
                'user_id': user.id,
                'username': data['username'],
                'create_time': str(user.member_since)
            }
        }
        return response_object,200
    else:
        response_object = {
            'status': 'fail',
            'message': 'User already exists. Please Log in.',
        }
        return response_object, 409


def get_all_users():
    return User.query.all()



def get_a_user(public_id):
    #return User.query.filter_by(public_id=public_id).first()
    pass


def save_changes(data):
    db.session.add(data)
    db.session.commit()



