from app.extensions import db
from app.auth.models import BaseModel, UserRoles,User,Role
from app.configs import ROLE_DICT


class Courses(db.Model, BaseModel):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(24), index=True)
    announcement_date = db.Column(db.String, nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean, default=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'))
    students = db.relationship('User', secondary='join(User,UserCourses).join(UserRoles)',
        secondaryjoin=f'UserRoles.role_id == {ROLE_DICT["student"]}',viewonly=True)

    lecturer = db.relationship('User', secondary='join(User,UserCourses).join(UserRoles)',
        secondaryjoin=f'UserRoles.role_id == {ROLE_DICT["lecturer"]}', viewonly=True)


class UserCourses(db.Model, BaseModel):
    __tablename__ = 'user_courses'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    courses_id = db.Column(db.Integer, db.ForeignKey('courses.id'))

    def __init__(self,user_id,courses_id):
        self.user_id = user_id
        self.role_id = courses_id


class Subject(db.Model, BaseModel):
    __tablename__ = 'subject'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(124), index=True)
    has_intership = db.Column(db.Boolean, default=False)
    courses = db.relationship('Courses', backref='subject')
    # sylabus