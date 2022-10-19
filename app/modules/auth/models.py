from app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app.settings import BaseConfig
from app.database import BaseModel


class User(db.Model, UserMixin, BaseModel):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    passport_id = db.Column(db.Integer, unique=True, index=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    last_name = db.Column(db.String(64), nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    birth_date = db.Column(db.String, nullable=False)
    gender = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(225))
    phone_number = db.Column(db.Integer,unique=True,index=True)
    country = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    region = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(125), nullable=False)
    role = db.relationship('Role',secondary='user_roles',backref='users')

    school_number = db.Column(db.Integer, nullable=True)
    school_class_number = db.Column(db.Integer, nullable=True)
    parent_name = db.Column(db.String(125), nullable=True)
    parent_mobile_number = db.Column(db.Integer,nullable=True)

    university = db.Column(db.String(125), nullable=True)
    degree = db.Column(db.String(64), nullable=True)
    education_level = db.Column(db.String(64), nullable=True)
    faculty = db.Column(db.String(64), nullable=True)
    program = db.Column(db.String(64), nullable=True)

    def __init__(self, name, last_name, email, password,  gender, birth_date,  phone_number, passport_id, country, city,
                 region, address, school_number=None, school_class_number=None, parent_name=None,
                 parent_mobile_number=None, university=None, degree=None, education_level=None, faculty=None,
                 program=None
                 ):
        self.name = name
        self.last_name = last_name
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.gender = gender
        self.birth_date = birth_date
        self.phone_number = phone_number
        self.passport_id = passport_id
        self.country = country
        self.city = city
        self.region = region
        self.address = address
        self.school_number = school_number
        self.school_class_number = school_class_number
        self.parent_name = parent_name
        self.parent_mobile_number = parent_mobile_number
        self.university = university
        self.degree = degree
        self.education_level = education_level
        self.faculty = faculty
        self.program = program

    @classmethod
    def find_by_email(cls, temp_email):
        email = cls.query.filter_by(email=temp_email).first()
        if email:
            return email

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'{self.name} {self.last_name}, {self.role}'

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(BaseConfig.SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(BaseConfig.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            print(e)
            return None
        return User.query.get(user_id)


class UserRoles(db.Model, BaseModel):
    __tablename__ = 'user_roles'

    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    role_id = db.Column(db.Integer,db.ForeignKey('role.id'))

    def __init__(self,user_id,role_id):
        self.user_id = user_id
        self.role_id = role_id


class Role(db.Model, BaseModel):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(24), unique=True, index=True, nullable=False)

    def __repr__(self):
        return self.name
