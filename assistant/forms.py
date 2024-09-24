from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class AssistantForm(FlaskForm):
    Name = StringField('Name', validators=[DataRequired()])
    OwnerID = StringField('OwnerID', validators=[DataRequired()])
    Parameter1 = StringField('Parameter1')
    Parameter2 = StringField('Parameter2')
    Parameter3 = StringField('Parameter3')
    Prompt = StringField('Prompt')
    IsTest = BooleanField('IsTest')
    submit = SubmitField('Submit')
