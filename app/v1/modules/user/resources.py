# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: resources.py
# @Date:   2018-08-18 17:00:27
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-24 00:08:55

from flask_restplus import Resource, Namespace

from app import db
from app.v1.model.user import User
from app.v1.extensions.auth import  role_required
from app.v1.extensions.auth.jwt_auth import  auth
from app.v1.utils.user_utils import get_all_users
from .serial import user_put_model,get_user_fields

user_ns = Namespace('user',description='user related operations')

parser = user_ns.parser()
parser.add_argument('Authorization', type=str,
                    location='headers',
                    help='Bearer Access Token',
                    required=True)

@user_ns.route('/')
class UserList(Resource):
    """
    列出所有用户
    过滤某个字段，在头部加上 X-Fields: email
    """
    @user_ns.doc('获取用户列表')
    @user_ns.marshal_list_with(get_user_fields,envelope='data')
    def get(self):
        return get_all_users()





@user_ns.route('/<email>')
class DeleterUserRequired(Resource):
    # 删除用户，只有超级管理员才有权限，请求时携带角色为sa的access_token
    @user_ns.doc('删除用户',parser=parser,)
    @auth.login_required
    @role_required.permission(2)
    def delete(self, email):
        user = User.query.filter_by(email=email).first()
        # Get user if it is existed.
        if user is not None:
            # Delete action.
            db.session.delete(user)
            db.session.commit()

            print ("user {} deleted".format(user.username))
            return {"message": "user {} delete success.".format(user.username)}, 200
        else:
            return {"message": "user {} does not exist.".format(email)}, 404

    @user_ns.expect(user_put_model,validate=True,location='body')
    @user_ns.doc('更新用户信息')
    def put(self):
        pass
