from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class HardwareForm(FlaskForm):
    manufacturer = StringField('Manufacturer', [DataRequired()])
    model = StringField('Model', [DataRequired()])
    serial_number = StringField('Serial Number', [DataRequired()])
    user_full_name = StringField('User full name', [DataRequired()])
    submit = SubmitField('Submit')
