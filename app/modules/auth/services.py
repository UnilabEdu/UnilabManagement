import string
import secrets
import datetime
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from app.settings import BaseConfig


def get_password():
    """Generate a random password."""

    symbols = ['*', '%', '?', '=', '+']
    password = ""
    for _ in range(4):
        password += secrets.choice(string.ascii_lowercase)
        password += secrets.choice(string.ascii_uppercase)
        password += secrets.choice(string.digits)
        password += secrets.choice(symbols)
    return password


def send_email_after_register(user, password):
    time_now = datetime.datetime.now()
    message = MIMEMultipart()

    # Get SMTP credentials & settings
    smtp_server = BaseConfig.SMTP_SERVER
    smtp_port = BaseConfig.SMTP_PORT
    smtp_email_address = BaseConfig.SMTP_EMAIL_ADDRESS
    smtp_email_password = BaseConfig.SMTP_EMAIL_PASSWORD

    message_text = 'Congratulations! Your successfully registered to Unilab\n Here is password for your account:' \
                   f'\n\n {password}'

    message['Subject'] = f'Registration Success Message - [Automated Email] {time_now.strftime("%d-%m-%Y")}'
    message['From'] = smtp_email_address
    message['To'] = user.email
    message.attach(MIMEText(message_text))

    server = smtplib.SMTP(smtp_server, smtp_port)
    # server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    # server.ehlo
    server.login(smtp_email_address, smtp_email_password)
    server.sendmail(smtp_email_address, user.email, message.as_string())
    server.quit()
