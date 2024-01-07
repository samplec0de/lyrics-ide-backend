import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(
        subject: str,
        message: str,
        from_name: str,
        from_email: str,
        to_email: str,
        smtp_server: str,
        smtp_port: str | int,
        smtp_user: str,
        smtp_password: str
):
    """Отправка электронной почты"""

    msg = MIMEMultipart()
    msg['From'] = f"{from_name} <{from_email}>"
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(message, 'plain'))

    server = smtplib.SMTP_SSL(smtp_server, smtp_port)
    server.login(smtp_user, smtp_password)

    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()


def lyrics_send_email(subject: str, message: str, to_email: str):
    """Отправка электронной почты с подстановкой переменных из окружения"""
    send_email(
        subject=subject,
        message=message,
        to_email=to_email,
        from_name=os.environ.get('SMTP_NAME'),
        from_email=os.environ.get('SMTP_EMAIL'),
        smtp_server=os.environ.get('SMTP_SERVER'),
        smtp_port=os.environ.get('SMTP_PORT'),
        smtp_user=os.environ.get('SMTP_USER'),
        smtp_password=os.environ.get('SMTP_PASSWORD')
    )
