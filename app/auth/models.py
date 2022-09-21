from enum import unique
from app import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class BaseModel:
    """
    This Class describe SQLAlchemy DB model with Basic CRUD functionality

    atribs:
        - id: primery key
        - create
        - update
        - delete
        - save
        - read
    """

    def create(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def update_to_db(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, UserMixin, BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, index=True)
    last_name = db.Column(db.String(64), nullable=False, index=True)
    email = db.Column(db.String(64), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(225))
    gender = db.Column(db.String(64), nullable=False)
    birth_date = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.Integer,unique=True,index=True)
    passport_id = db.Column(db.Integer,unique=True,index=True)
    country = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    region = db.Column(db.String(64), nullable=False)
    address = db.Column(db.String(125), nullable=False)
    role = db.Column(db.String(64), nullable=False)

    school_number = db.Column(db.Integer, nullable=True)
    school_class_number = db.Column(db.Integer, nullable=True)
    parent_name = db.Column(db.String(125), nullable=True)
    parent_mobile_number = db.Column(db.Integer)

    university = db.Column(db.String(125), nullable=True)
    degree = db.Column(db.String(64), nullable=True)
    education_level = db.Column(db.String(64), nullable=True)
    faculty = db.Column(db.String(64), nullable=True)
    program = db.Column(db.String(64), nullable=True)

    def __init__(self, name, last_name, email,password,  gender,birth_date,  phone_number, passport_id, country, city,
                    region, address, role, school_number=None, school_class_number=None, parent_name=None,
                    parent_mobile_number=None, university=None,
                    degree=None, education_level=None, faculty=None, program=None):
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
        self.role = role
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
        return check_password_hash(self.password_hash(), password)

    def __repr__(self):
        return f'{self.name} {self.last_name}, {self.role}, are created'

