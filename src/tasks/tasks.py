import smtplib
from email.message import EmailMessage

from celery import Celery
from src.config import SMTP_USER, SMTP_PASS


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker="redis://localhost:6379")


def create_email(username: str, user_mail: str):
    email = EmailMessage()
    email["Subject"] = "Real Estate"
    email["From"] = SMTP_USER
    email["To"] = user_mail

    email.set_content(
        "<div>"
        f'''<h1>Здравствуйте, {username}!</h1>'''
        "</div>",
        subtype="html"
    )
    return email


@celery.task
def send_email(username: str, user_mail: str):
    email = create_email(username, user_mail)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)
