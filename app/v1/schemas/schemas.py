# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: schemas.py
# @Date:   2018-08-14 21:04:02
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-17 16:12:55

from marshmallow import Schema, fields


# class BaseUserSchema(Schema):

#     """
#         Base user schema returns all fields but this was not used in user handlers.
#     """

#     # Schema parameters.

#     id = fields.Int(dump_only=True)
#     username = fields.Str()
#     email = fields.Str()
#     password = fields.Str()

class UserSchema(Schema):
    # Schema parameters.
    id = fields.Int(dump_only=True)
    username = fields.Str()
    email = fields.Email()
    user_role = fields.Str()
    member_since = fields.DateTime()



