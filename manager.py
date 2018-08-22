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
from livereload import Server

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

@manager.command
def dev():
    live_server = Server(app.wsgi_app)
    live_server.watch('**/*.*')
    live_server.serve(open_url=False,port=5000,debug=True)


if __name__ == '__main__':
    manager.run()
