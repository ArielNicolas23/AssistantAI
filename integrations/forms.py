from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class IntegrationForm(FlaskForm):
    # OwnerID = StringField('OwnerID', validators=[DataRequired()])
    Type = StringField('Type', validators=[DataRequired()])
    IsTest = BooleanField('IsTest')
    submit = SubmitField('Submit')

class IntegrationUpdateForm(FlaskForm):
    # OwnerID = StringField('OwnerID', validators=[DataRequired()])
    Type = StringField('Type', validators=[DataRequired()])
    MetaUserToken = StringField('MetaUserToken', validators=[DataRequired()])
    MetaUserID = StringField('MetaUserID', validators=[DataRequired()])
    MetaPageID = StringField('MetaPageID', validators=[DataRequired()])
    MetaPageName = StringField('MetaPageName', validators=[DataRequired()])
    AssistantID = StringField('AssistantID', validators=[DataRequired()])
    IsTest = BooleanField('IsTest')
    submit = SubmitField('Submit')
