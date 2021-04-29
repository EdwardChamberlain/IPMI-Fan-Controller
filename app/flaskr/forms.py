from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange


class Fanspeed_Form(FlaskForm):
    speed = IntegerField('Speed Percentage', validators=[NumberRange(min=10, max=100, message="Value must be between 10% and 100%"), DataRequired()])
    submit = SubmitField('Apply')


class Configure_Form(FlaskForm):
    host = StringField("IPMI Hostname")
    user = StringField("IPMI Username")
    passwd = PasswordField("IPMI Password")
    
    submit_configure = SubmitField('Apply')


class StartUp_Form(FlaskForm):
    choices = [
        ('', ''),
        ('True', 'Enable'),
        ('False', 'Disable'),
    ]

    enable = SelectField("Startup Script", choices=choices)
    manual_mode = SelectField("Manual Mode", choices=choices)
    fan_speed = StringField('Fan Speed Percentage')

    submit_startup = SubmitField('Save')