from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class IntegrationForm(FlaskForm):
    OwnerID = StringField('OwnerID', validators=[DataRequired()])
    Type = StringField('Type', validators=[DataRequired()])
    Token = StringField('Token', validators=[DataRequired()])
    AssistantID = StringField('AssistantID', validators=[DataRequired()])
    IsTest = BooleanField('IsTest')
    submit = SubmitField('Submit')
