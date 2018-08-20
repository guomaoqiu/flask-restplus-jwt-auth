# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: auth.py
# @Date:   2018-08-14 21:04:02
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-20 23:11:57

from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as JWT

# JWT creation.
jwt = JWT('top secret!', expires_in=930)

# Refresh token creation.
refresh_jwt = JWT('telelelele', expires_in=17200)

# Email token creation
#refresh_jwt = JWT('telelelele', expires_in=17200)


# Auth object creation.
auth = HTTPTokenAuth('OAuth')

