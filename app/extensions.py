from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import string
import secrets
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "auth.login"





def get_password():
    symbols = ['*', '%', '?','=','+']
    password = ""
    for _ in range(4):
        password += secrets.choice(string.ascii_lowercase)
        password += secrets.choice(string.ascii_uppercase)
        password += secrets.choice(string.digits)
        password += secrets.choice(symbols)
    return password

def send_email_after_register(user,password):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import datetime
    now = datetime.datetime.now()

    SERVER = os.environ.get('SMTP_SERVER') or 'smtp.gmail.com' # "your smtp server"
    PORT = 587 # your port number
    FROM =  os.environ.get('EMAIL_ADDRESS') or 'unilab@gmail.com'
    TO = user.email # "your to email ids"  # can be a list
    PASS = os.environ.get('EMAIL_PASSWORD') 

    message = MIMEMultipart()
    message['Subject'] = 'Registration Success Message - [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(
    now.year)

    message['From'] = FROM
    message['To'] = TO

    text = f'Your registration to Unilab has been successed, Welcome! \n\
        this is your password: \n\
            {password}'
    message.attach(MIMEText(text))
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


def send_email(subject, text, user):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import datetime
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