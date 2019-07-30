from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,FileField,TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User

class PostForm(FlaskForm):
    text = TextAreaField('text', validators=[DataRequired()],render_kw={'rows':'4'})
    submit = SubmitField('Submit',render_kw={'class': 'ui small green button'})
    #upload = SubmitField('Upload and Submit',render_kw={'class': 'ui small green button'})
    postimage = FileField('upload image')

class UploadUserImageForm(FlaskForm):

    userimage = FileField('Image file',validators=[DataRequired()])
    upload = SubmitField('Upload')

class RelationForm(FlaskForm):

    addfriend = SubmitField('Add Friend')

#DataRequired - it cannot be empty
class RegistrationForm(FlaskForm):
    name = StringField('name',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    'checks whether the database already has this name'
    def validate_name(self,name):
        user = User.query.filter_by(name = name.data).first()
        if user:
            raise ValidationError('That username is taken.')
            
    'checks whether the database already has this email'
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user:
            raise ValidationError('That email is taken.')

class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')
