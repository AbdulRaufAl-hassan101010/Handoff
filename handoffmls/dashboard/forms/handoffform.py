from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, widgets, SelectMultipleField
from wtforms.validators import DataRequired, Length


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
