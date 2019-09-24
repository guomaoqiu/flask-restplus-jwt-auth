# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: user_utils.py
# @Date:   2018-08-23 11:03:15
# @Last Modified by:   guomaoqiu
# @Last Modified time: 2019-09-24 10:54:49
import datetime
import uuid
from flask import url_for
from app import db
from app.v1.model.user import User
from validate_email import validate_email
from app.v1.mail.email import send_email
from app.v1.errors import CustomFlaskErr as notice

def save_new_user(data):
    user = User.query.filter_by(email=data['email']).first()
    print (data['username'])
    # validate_email: 用于检测邮箱是否正确，并且真实可用
    if not validate_email(data['email'],verify=True,check_mx=True):
        raise notice(status_code=500,return_code=20006,action_status=False)
    
    if not data['password']  or  not data['username']:
        raise notice(status_code=422,return_code=20007,action_status=False)

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

        email_confirm_token =  (user.generate_confirmation_token(data['email'],data['username']))

        confirm_url = (url_for('v1_blueprint.confirm',confirm_token=email_confirm_token,_external=True)) + '?email=' + data['email']

        # send confirm email to register user.
        # send_email(to=data['email'], subject='active',template='email_tpl/confirm', confirm_url=confirm_url,user=data['username'],)

        raise notice(status_code=200,return_code=30001,action_status=True,playbook={
                    'username': data['username'],
                    'create_time': str(user.member_since),
                    'confirm_url': str(confirm_url),
        })
    else:
        raise notice(status_code=409,return_code=20004)


def get_all_users():
    return User.query.all()



def get_a_user(public_id):
    #return User.query.filter_by(public_id=public_id).first()
    pass


def save_changes(data):
    db.session.add(data)
    db.session.commit()



