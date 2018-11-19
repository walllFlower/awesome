from . import mail
from flask import current_app, render_template
from flask_mail import Message
from threading import Thread

def send_async_msg(app, msg):
    with app.app_context():
        mail.send(msg)

# 异步发送邮件
def send_msg(to, subject, template, **kwargs):
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,
                  sender=current_app.config['FLASKY_MAIL_SENDER'],
                  recipients=['<zengymf@yonyou.com>'])
    msg.body = render_template(template + '.txt' , **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_msg, args=[current_app._get_current_object(), msg])
    thr.start()
    return thr
