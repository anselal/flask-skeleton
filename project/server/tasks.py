from smtplib import SMTPException

from flask import render_template
from flask_mail import Message
from flask_socketio import SocketIO

from project.server import celery, mail

@celery.task
def send_email(subject, template, recipients, **kwargs):
    socketio = SocketIO(message_queue='redis://')
    message = Message(subject)

    if isinstance(recipients, list):
        message.recipients = recipients
    elif isinstance(recipients, str):
        message.add_recipient(recipients)

    message.html = render_template('mails/' + template + '.html', **kwargs)

    try:
        mail.send(message)
    except SMTPException as e:
        socketio.emit('client notification', {'data': str(e), 'result': 'error'}, namespace='/test')
