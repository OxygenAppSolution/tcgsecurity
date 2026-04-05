from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email

class ContactForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired()])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    message = TextAreaField('Security Requirements', validators=[DataRequired()])
    submit = SubmitField('Request a Quote')