from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from handoffmls.models.lab import Lab


class RegistrationForm(FlaskForm):
    name = StringField('Name',
                       validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_name(self, name):
        instituition = Lab.query.filter_by(name=name.data).first()
        if instituition:
            raise ValidationError(
                'That name is taken. Please choose a different one.')

    def validate_email(self, email):
        instituition = Lab.query.filter_by(email=email.data).first()
        if instituition:
            raise ValidationError(
                'That email is taken. Please choose a different one.')
