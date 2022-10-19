from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, DateField, BooleanField
from wtforms.validators import DataRequired


class CoursesForm(FlaskForm):

    type = StringField('Course Type')

    announcement_date = DateField()
    start_date = DateField('Start Date', [DataRequired()])
    end_date = DateField('End Date')
    active = BooleanField('Active')
    submit = SubmitField('Submit')


class SubjectForm(FlaskForm):

    name = StringField('Subject Name', [DataRequired()])
    has_internship = BooleanField('Has Internship', default=False)
    syllabus = FileField('Syllabus', [FileAllowed(['docx', 'doc', 'odt', 'txt'])])
    submit = SubmitField('Submit')
