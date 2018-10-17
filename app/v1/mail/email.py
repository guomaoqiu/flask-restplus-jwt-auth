# -*- coding: utf-8 -*-
# @Author: guomaoqiu
# @File Name: sendmail.py
# @Date:   2018-08-18 22:45:33
# @Last Modified by:   Green
# @Last Modified time: 2018-10-15 18:33:38
from threading import Thread
from flask import current_app, render_template
from flask_mail import Mail, Message


def send_async_email(app, msg):
    with app.app_context():
        mail = Mail(app)
        mail.init_app(app)
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()

    msg = Message(app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['FLASKY_MAIL_SENDER'], recipients=[to],charset="utf8")

    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app,  msg])
    thr.start()
    return thr
