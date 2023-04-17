import smtplib
from email.message import EmailMessage

from celery import Celery
from src.config import SMTP_USER, SMTP_PASS


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker="redis://localhost:6379")


def create_email(username: str):
    email = EmailMessage()
    email["Subject"] = "Real Estate"
    email["From"] = SMTP_USER
    email["To"] = SMTP_USER

    email.set_content(
        "<div>"
        f'''<h1>Здравствуйте, {username}!</h1>'''
        "</div>",
        subtype="html"
    )
    return email


@celery.task
def send_email(username: str):
    email = create_email(username)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)
