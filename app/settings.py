import os


PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


ROLE_DICT = {
    'admin': 1,
    'lecturer': 2,
    'intern': 3,
    'student': 4
}


class BaseConfig(object):
    """Base configuration."""

    PROJECT_NAME = "Unilab_Admin_Panel"
    PROJECT_ROOT = PROJECT_ROOT
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(PROJECT_ROOT, 'db.sqlite')
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'asd;lkajs-90 as;doaksdasd02 ;;/A'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SMTP_SERVER = os.environ.get('SMTP_SERVER') or 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS') or 'unilab@gmail.com'
    SMTP_EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
