from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,EmailField,PasswordField,SelectField,DateField,TelField, BooleanField
from wtforms.validators import DataRequired,Email, Length,ValidationError
from app.modules.auth.models import User


class RegisterForm(FlaskForm):
    """User Registration Form"""

    first_name = StringField('First Name', [DataRequired()])
    last_name = StringField('Last Name', [DataRequired()])
    email = EmailField('Email', [Email(), DataRequired()])
    sex = SelectField(u'Sex', [DataRequired()], choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
    birth_date = DateField('Birth Date', [DataRequired()])
    phone_number = TelField('Phone Number', [DataRequired()])
    passport_id = StringField('ID Number', [Length(min=11, max=11), DataRequired()])
    country = StringField('Country', [DataRequired()])
    region = StringField('Region', [DataRequired()])
    city = StringField('City', [DataRequired()])
    address = StringField('Address', [DataRequired()])
    status = SelectField(
        'Choose Your Status', [DataRequired()], choices=[
                ('pupil', 'მოსწავლე'), ('student', 'სტუდენტი'), ('other', 'სხვა')
            ]
    )

    submit = SubmitField('Create Account')

    def validate_email_address(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            raise ValidationError('Email Address already exists! Please try a different email address')

    def validate_phone_number(self, phone_number):
        phone_number = User.query.filter_by(phone_number=phone_number.data).first()
        if phone_number:
            raise ValidationError('Phone number already exists! Please try different one!')

    def validate_passport_id(self, passport_id):
        passport_id = passport_id.data

        if not passport_id.isnumeric():
            raise ValidationError('Personal ID Should be numbers')

        passport_id = User.query.filter_by(passport_id=passport_id).first()

        if passport_id:
            raise ValidationError('Personal ID already exists! Please check and try again!')

    # school_number = IntegerField('School Number')
    # school_class_number = IntegerField('School Class Number')
    # parent_name = StringField('Parent First Name')
    # parent_mobile_number = TelField('Parent Phone Number')

    # university = StringField('university name')
    # degree = StringField('Degree')
    # education_level = SelectField(u'Education Level',
    #     choices=[('1', '1'), ('2', '2'), ('3', '3'),('4','4')])
    # faculty = StringField('Faculty')
    # program = StringField('Program')


class LoginForm(FlaskForm):
    """User Login Form"""

    email = EmailField('Email',validators=[Email(),DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField("Sign in")
