# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: user.py
# @Date:   2018-08-18 17:00:27
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-21 23:05:38
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

parser = user_ns.parser()
parser.add_argument('Authorization', type=str, \
					location='headers',help='Bearer Access Token',required=True)

@user_ns.route('/delete_user/<email>')
class DeleterUserRequired(Resource):
    # 删除用户，只有超级管理员才有权限，请求时携带角色为sa的access_token
    @user_ns.doc(parser=parser)
    @auth.login_required
    @role_required.permission(2)
    def delete(self,email):
        user = User.query.filter_by(email=email).first()
        # Get user if it is existed.
        if user is not None:
            # Delete action.
            db.session.delete(user)
            db.session.commit()

            print "user {} deleted".format(user.username)
            return {"message": "user {} delete success.".format(user.username)},200
        else:
            return {"message": "user {} does not exist.".format(email)},404


                      