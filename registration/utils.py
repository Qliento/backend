from django.core.mail import EmailMessage
import os
from qliento import settings
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


class Util:
    @staticmethod
    def send_email(data):

        message = Mail(
            from_email='qlientoinfo@gmail.com',
            to_emails=[data['to_email']],
            subject=data['email_subject'],
            html_content=data['email_body'],
            )

        try:
            sg = SendGridAPIClient(settings.api_key)
            response = sg.send(message)

        except Exception as e:
            pass
