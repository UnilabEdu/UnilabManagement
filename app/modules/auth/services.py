import string
import secrets
import datetime
import smtplib
import os

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


def send_email(subject, text, user):


    now = datetime.datetime.now()

    SERVER = os.environ.get('SMTP_SERVER') or 'smtp.gmail.com'
    PORT = 587
    FROM =  os.environ.get('EMAIL_ADDRESS') or 'unilab@gmail.com'
    TO = user.email
    PASS = os.environ.get('EMAIL_PASSWORD') 
    message = MIMEMultipart()
    message['Subject'] = subject

    message['From'] = FROM
    message['To'] = TO

    text_message = f'{text}'
    message.attach(MIMEText(text_message))
    print('Initiating Server...')

    server = smtplib.SMTP(SERVER, PORT)
    #server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.set_debuglevel(1)
    server.ehlo()
    server.starttls()
    #server.ehlo
    server.login(FROM, PASS)
    server.sendmail(FROM, TO, message.as_string())

    print('Email Sent...')

    server.quit()
