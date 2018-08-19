# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: user.py
# @Date:   2018-08-18 17:00:27
# @Last Modified by:   Green
# @Last Modified time: 2018-08-19 00:09:38
from flask_restplus import Resource, Namespace

user_ns = Namespace('user')


@user_ns.route('/hello')
class HelloUser(Resource):
    def get(self):
        return {'hello': 'I am a user'}
