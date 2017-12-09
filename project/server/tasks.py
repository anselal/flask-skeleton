from flask_mail import Message

from project.server import celery, mail, app

@celery.task
def send_email():
    with app.app_context():
        message = Message('Hello from flask',
                        recipients=['hanisek.sedlon@gmail.com'])
        message.body = 'Hello :)'
        mail.send(message)