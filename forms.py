from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    text = StringField('text', validators=[DataRequired()])
    upload = SubmitField('Upload')