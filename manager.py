# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: manager.py
# @Date:   2018-08-18 22:45:33
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-21 15:16:37

import os
from app import create_app, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app.v1.model import user,blacklist

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

#
# @manager.command
# def run():
#     app.run(use_reloader=True,debug=True)

if __name__ == '__main__':
    #app.run(use_reloader=True,debug=True)
    manager.run()
