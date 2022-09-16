from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import string
import secrets

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

def send_email_after_register(email_to,password):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    import datetime
    now = datetime.datetime.now()

    SERVER = 'smtp.gmail.com' # "your smtp server"
    PORT = 587 # your port number
    FROM =  'unilab@gmail.com' # "your from email id"
    TO = email_to # "your to email ids"  # can be a list
    PASS = '***********' # "your email id's password"

    message = MIMEMultipart()
    message['Subject'] = 'Registration Success Message - [Automated Email]' + ' ' + str(now.day) + '-' + str(now.month) + '-' + str(
    now.year)

    message['From'] = FROM
    message['To'] = TO

    text = 'Your registration to Unilab has been successed, Welcome \n this is your password {}'.format(password)
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