from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from handoffmls.models.lab import Lab
from handoffmls.models.user import User


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


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class AddUserForm(FlaskForm):
    first_name = StringField('First name',
                             validators=[DataRequired(), Length(min=2, max=30)])
    last_name = StringField('Last name',
                            validators=[DataRequired(), Length(min=2, max=30)])
    other_name = StringField('Other name')
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    confirm_password = PasswordField('Confirm Password')
    submit = SubmitField('Add User')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose a different one.')


class CreateHandoffForm(FlaskForm):
    summary = TextAreaField('Summary',
                            validators=[DataRequired(), Length(min=5)])
    actions = TextAreaField('Actions',
                            validators=[DataRequired(), Length(min=5)])
    changes = TextAreaField('Changes', validators=[DataRequired()])
    evaluation = TextAreaField('Evaluation',
                               validators=[DataRequired()])
    persons = SelectMultipleField('Names or Crew', option_widget=widgets.CheckboxInput(
    ), widget=widgets.ListWidget(prefix_label=False))
    submit = SubmitField('Create Handoff')
