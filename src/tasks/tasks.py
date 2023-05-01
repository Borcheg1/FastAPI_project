import smtplib
from email.message import EmailMessage

from celery import Celery
from src.config import SMTP_USER, SMTP_PASS


SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 465

celery = Celery("tasks", broker="redis://localhost:6379")


def create_verify_email(username: str, user_mail: str, token: str):
    email = EmailMessage()
    email["Subject"] = "Real Estate"
    email["From"] = SMTP_USER
    email["To"] = user_mail

    email.set_content(
        "<div>"
        f'''<h2>Здравствуйте, {username}!</h2>'''
        f'''<p>Для подтверждения электронной почты перейдите по ссылке</p>'''
        f'''<a href='http://127.0.0.1:8000/auth/verify?token={token}' target='_blank'>Подтвердить электронную почту</a>'''
        "</div>",
        subtype="html"
    )
    return email


def create_reset_pass_email(username: str, user_mail: str, token: str):
    email = EmailMessage()
    email["Subject"] = "Real Estate"
    email["From"] = SMTP_USER
    email["To"] = user_mail

    email.set_content(
        "<div>"
        f'''<h2>Здравствуйте, {username}!</h2>'''
        f'''<p>Ваш токен для смены пароля:</p>'''
        f'''<p>{token}</p>'''
        "</div>",
        subtype="html"
    )
    return email


@celery.task
def send_verify_email(username: str, user_mail: str, token: str):
    email = create_verify_email(username, user_mail, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)


@celery.task
def send_reset_pass_email(username: str, user_mail: str, token: str):
    email = create_reset_pass_email(username, user_mail, token)
    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as server:
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(email)
