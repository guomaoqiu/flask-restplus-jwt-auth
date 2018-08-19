# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: manager.py
# @Date:   2018-08-18 22:45:33
# @Last Modified by:   Green
# @Last Modified time: 2018-08-19 00:23:38

import os
from app import create_app, db
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from livereload import Server
# from flask import url_for,render_template,redirect

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
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
