# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: __init__.py
# @Date:   2018-08-19 00:08:41
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-22 00:03:38
from flask import Blueprint
from flask_restplus import Api


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
            description='auth: guomaoqiu', 
            contact="Author",
            contact_email="2399447849@qq.com",
            default="auth", 
            default_label=None
            # authorizations=authorizations,
            # security='apiKey')
            )


from .resources.auth import auth_ns
from .resources.user import user_ns


v1_api.add_namespace(auth_ns)
v1_api.add_namespace(user_ns)


