# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: role_required.py
# @Date:   2018-08-18 22:04:29
# @Last Modified by:   Green
# @Last Modified time: 2018-08-19 11:58:42
import logging
import functools
from app.v1 import errors as error
from flask import request
from app.v1.conf.auth import jwt


def permission(arg):

    def check_permissions(f):

        @functools.wraps(f)
        def decorated(*args, **kwargs):

            # Get request authorization.
            auth = request.authorization
            print auth

            # Check if auth is none or not.
            if auth is None and 'Authorization' in request.headers:

                try:
                    # Get auth type and token.
                    auth_type, token = request.headers['Authorization'].split(None, 1)
                    print auth_type,token
                    # Generate new token.
                    data = jwt.loads(token)
                    print data


                    # Check if admin
                    if data['admin'] < arg:

                        # Return if user is not admin.
                        return error.NOT_ADMIN

                except ValueError:
                    # The Authorization header is either empty or has no token.
                    return error.HEADER_NOT_FOUND

                except Exception as why:
                    # Log the error.
                    logging.error(why)

                    # If it does not generated return false.
                    return error.INVALID_INPUT_422

            # Return method.
            return f(*args, **kwargs)

        # Return decorated method.
        return decorated

    # Return check permissions method.
    return check_permissions
