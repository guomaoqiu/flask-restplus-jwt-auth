# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: errors.py
# @Date:   2018-08-18 17:17:43
# @Last Modified by:   Green
# @Last Modified time: 2018-10-10 11:32:20

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

error_list = {
    # 成功状态码 
    0: "成功",

    # 用户错误：
    20001: "用户不存在",
    20002: "账号已被禁用",
    20003: "密码无效",
    20004: "用户已存在",
    20005: "用户未登录",
    20006: "邮箱地址无效",
    20007: "用户名、密码不能为空",

    # 参数错误：
    10001: "参数为空",
    10002: "参数无效",
    10003: "参数类型错误",
    10004: "参数缺失",
}


# 参数错误：10001-19999 */
PARAM_IS_INVALID = ({"message": "参数无效", "return_code": 10001 })
PARAM_IS_BLANK = ({"message": "参数为空", "return_code": 10002 })
PARAM_TYPE_BIND_ERROR = ({"message": "参数类型错误", "return_code": 10003 })
PARAM_NOT_COMPLETE = ({"message": "参数缺失", "return_code": 10004 })

# 用户错误：20001-29999*/
USER_NOT_LOGGED_IN = ({"message": "用户未登录", "return_code": 20001 })
USER_LOGIN_ERROR = ({"message": "账号不存在或密码错误", "return_code": 20002,})
USER_ACCOUNT_FORBIDDEN = ({"message": "账号已被禁用", "return_code":20003})
USER_NOT_EXIST = ({"message": "用户不存在xxxxxxxxxxx", "return_code": 20004 })
USER_HAS_EXISTED = ({"message": "用户已存在", "return_code": 20005})

# 业务错误：30001-39999 
#SPECIFIED_QUESTIONED_USER_NOT_EXIST(30001, "某业务出现问题"})

# # 系统错误：40001-49999 */
# SYSTEM_INNER_ERROR(40001, "系统繁忙，请稍后重试"),

# # 数据错误：50001-599999 */
# RESULE_DATA_NONE(50001, "数据未找到"),
# DATA_IS_WRONG(50002, "数据有误"),
# DATA_ALREADY_EXISTED(50003, "数据已存在"),

# # 接口错误：60001-69999 */
# INTERFACE_INNER_INVOKE_ERROR(60001, "内部系统接口调用异常"),
# INTERFACE_OUTTER_INVOKE_ERROR(60002, "外部系统接口调用异常"),
# INTERFACE_FORBID_VISIT(60003, "该接口禁止访问"),
# INTERFACE_ADDRESS_INVALID(60004, "接口地址无效"),
# INTERFACE_REQUEST_TIMEOUT(60005, "接口请求超时"),
# INTERFACE_EXCEED_LOAD(60006, "接口负载过高"),

# # 权限错误：70001-79999 */
# PERMIS


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
        {   'status': 403,
            'message': '未授权访问'
        }), 403)



class CustomFlaskErr(Exception):
    status_code = 400
    def __init__(self,status_code=None,return_code=None):
        super().__init__(self)
        self.return_code = return_code
        self.status_code = status_code
       
    def to_dict(self):
        rv = dict()
        rv['message'] = error_list.get(self.return_code)
        rv['return_code'] = self.return_code
        rv['status_code'] = self.status_code
        print(rv)
        return rv

@v1_blueprint.app_errorhandler(CustomFlaskErr)
def handle_flask_error(error):
    # response 的 json 内容为自定义错误代码和错误信息
    response = jsonify(error.to_dict())
    # response 返回 error 发生时定义的标准错误代码
    response.status_code = error.status_code
    print(response)

    return response

