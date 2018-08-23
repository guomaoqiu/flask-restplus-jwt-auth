# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: blacklist.py
# @Date:   2018-08-23 22:48:54
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-23 22:49:23
from app import db
# 过期refresh token
class Blacklist(db.Model):
    # Generates default class name for table. For changing use

    # Blacklist id.
    id = db.Column(db.Integer, primary_key=True)

    # Blacklist invalidated refresh tokens.
    refresh_token = db.Column(db.String(length=255))

    def __repr__(self):
        # This is only for representation how you want to see refresh tokens after query.
        return "<User(id='%s', refresh_token='%s', status='invalidated.')>" % (
            self.id, self.refresh_token)
