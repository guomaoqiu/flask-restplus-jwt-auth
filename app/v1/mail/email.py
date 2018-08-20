# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: email.py
# @Date:   2018-08-14 23:22:24
# @Last Modified by:   guomaoqiu@sina.com
# @Last Modified time: 2018-08-19 23:44:31

from threading import Thread
from flask import current_app, render_template
from flask_mail import Mail, Message

def send_async_email(app, msg):
    with app.app_context():
        mail = Mail(app)
        mail.init_app(app)
        mail.send(msg)

def send_email(to, subject,template, **kwargs):
    app = current_app._get_current_object()
 
    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    #print msg
    return thr
