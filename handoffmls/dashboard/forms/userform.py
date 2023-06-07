from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from handoffmls.models.user import User


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
