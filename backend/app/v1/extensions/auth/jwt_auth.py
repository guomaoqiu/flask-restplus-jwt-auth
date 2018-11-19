# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: jwt_auth.py
# @Date:   2018-08-23 19:26:56
# @Last Modified by:   Green
# @Last Modified time: 2018-10-10 16:34:32

from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

# JWT creation.
jwt = JWT('UbuQgGIdry*H&&I@', expires_in=6000)


# Refresh token creation.
refresh_jwt = JWT('Ag93ZQ3KcGg&KUhR', expires_in=17200)

# Email token creation
confirm_email_jwt = JWT('HuGIUMKXLoHi4Y2S', expires_in=17200)

# Auth object creation.
auth = HTTPTokenAuth('Bearer')

