# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: role_required.py
# @Date:   2018-08-18 22:04:29
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-21 18:45:17
import logging
import functools
from flask import request
from app.v1.extensions.auth.jwt_auth import jwt


def permission(arg):

    def check_permissions(f):

        @functools.wraps(f)
        def decorated(*args, **kwargs):

            # Get request authorization.
            # 获取请求认证
            auth = request.authorization
            # Check if auth is none or not.
            if auth is None and 'Authorization' in request.headers:

                try:
                    # 获取auth type 跟 token.
                    auth_type, token = request.headers['Authorization'].split(None, 1)
                    
                    # 反序列化 token
                    data = jwt.loads(token)
                    print data

                    if data['admin'] == 2:
                        print ("Your role is sa .")
                    elif data['admin'] == 1:
                        print ("Your role is admin .")
                    else:
                        print ("Your role is user .".format(data['admin']))

                    # permission_level来判断权限
                    if data['admin'] < arg:

                        # 如果用户不是对应的角色.
                        return  {"message": "Permission denied, your role code is {} .".format(data['admin'])}, 403 

                except ValueError:
                    # The Authorization header is either empty or has no token.
                    return {"message": "Headr Not Found ."}, 404

                except Exception as why:
                    # Log the error.
                    logging.error(why)

                    # If it does not generated return false.
                    return {"message": "Invalid input ."}, 422 

            # Return method.
            return f(*args, **kwargs)

        # Return decorated method.
        return decorated

    # Return check permissions method.
    return check_permissions
