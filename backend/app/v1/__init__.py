# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: __init__.py
# @Date:   2018-08-19 00:08:41
# @Last Modified by:   guomaoqiu
# @Last Modified time: 2019-09-24 09:47:29
from flask import Blueprint
from flask_restplus import Api

# v1 公共蓝图
# 直接制定了templates的路径，如果不指定，则需要将app/v1下面的tempates放到app目录下
v1_blueprint = Blueprint('v1_blueprint', __name__,
                        template_folder='templates')

# Bases Authorization
# authorizations = {
#     'apiKey': {
#         'type': 'apiKey',
#         'in': 'header',
#         'name': 'Authorization'
#     }
# }

v1_api = Api(v1_blueprint,
            title='DevOps FlaskREST API',
            version='1.0',
            description='auth: guomaoqiu\n'
                        'since: 2019-08-01',
            contact="Author",
            contact_email="2399447849@qq.com",
            default="auth", 
            default_label=''
            #authorizations='authorizations',
            #security='apiKey'
            )

# 导入两个红图

from .modules.auth.resources import auth_ns
from .modules.user.resources import user_ns
from .modules.test.resources import test_ns

v1_api.add_namespace(auth_ns)
v1_api.add_namespace(user_ns)
v1_api.add_namespace(test_ns)




