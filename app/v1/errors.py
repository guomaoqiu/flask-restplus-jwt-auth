# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: errors.py
# @Date:   2018-08-18 17:17:43
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-22 01:00:39

# 200 OK - [GET]：服务器成功返回用户请求的数据
# 201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功
# 202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
# 204 NO CONTENT - [DELETE]：用户删除数据成功
# 400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作
# 401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）
# 403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的
# 404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作
# 406 Not Acceptable - [GET]：用户请求的格式不可得
# 410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的
# 422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误
# 500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功
from flask import make_response,jsonify
from app.v1 import v1_blueprint
from app.v1.extensions.auth.jwt_auth import auth

SERVER_ERROR_500 = ({"message": "An error occured."}, 500)
NOT_FOUND_404 = ({"message": "Resource could not be found."}, 404)
NO_INPUT_400 = ({"message": "No input data provided."}, 400)
INVALID_INPUT_422 = ({"status":1,"message": "Invalid input."}, 422)

PASSWORD_INVALID_421 = ({"message": "Invalid password."}, 421)
ALREADY_EXIST = ({"status":1,"message": "Already exists."}, 409)

DOES_NOT_EXIST = ({"message": "Does not exists."}, 409)
NOT_ADMIN = ({"message": "Admin permission denied."}, 998)
HEADER_NOT_FOUND = ({"message": "Header does not exists."}, 999)


# 自定义错误提示
@auth.error_handler
def unauthorized():
    return make_response(jsonify(
    	{	'status': 403,
    		'message': 'Unauthorized Access'
    	}), 403)




