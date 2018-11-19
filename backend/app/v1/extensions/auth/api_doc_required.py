# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: api_doc_required.py
# @Date:   2018-08-19 23:42:48
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-23 22:48:40

from flask import request
from functools import wraps 

def permission(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        token = None
        if 'X-API-KEY' in request.headers:
            token = request.headers['X-API-KEY']

        if not token:
            return {'message' : 'Token is missing.'}, 401

        if token != 'mytoken':
            return {'message' : 'Your token is wrong, wrong, wrong!!!'}, 401

        print('TOKEN: {}'.format(token))
        return f(*args, **kwargs)

    return decorated