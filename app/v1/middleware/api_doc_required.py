# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: api_doc_required.py
# @Date:   2018-08-19 01:42:22
# @Last Modified by:   Green
# @Last Modified time: 2018-08-19 02:51:04
#
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