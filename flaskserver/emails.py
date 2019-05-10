from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from flaskserver.extensions import mail
import os
import sendgrid
#from sendgrid.helpers.mail import *

def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)

def send_mail(subject, to ,body):#to, subject, body
    message = Message(subject, recipients=[to], body=body)
    mail.send(message)
    # sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    # from_email = Email('noreply@helloflask.com')
    # to_email = Email('yukuaifeng@hotmail.com')
    # subject = 'hello, yukuaifeng'
    # content = Content('text/plain', 'hello,yukuifeng ,this is email sender test!')
    # mail = Mail(from_email, subject, to_email, content)
    # print(mail.get())
    # response = sg.client.mail.sent.post(request_body=mail.get())
    # print(response.body)
    # to_email = Email(to)
    # content = Content("text/plain", body)
    # mail = Mail(from_email, subject, to_email, content)
    # response = sg.client.mail.send.post(request_body=mail.get())


def send_confirm_email(user, token):
    # body = render_template('emails/confirm.html', user=user, token=token)
    # send_mail(subject='Email Confirm', to=user.email, body=body)
    send_mail()

