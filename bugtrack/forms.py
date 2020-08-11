from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, Email, ValidationError
from bugtrack.models import User



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email taken. Choose different email.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username taken. Choose different username.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_user = BooleanField('Remember Me')
    submit = SubmitField('Login')

class IssueForm(FlaskForm):
    issue_title = StringField('What`s up', validators=[DataRequired()])
    issue_type = RadioField('How bad is it?', choices=[(1, 'Critical'), (2, 'Severe'), (3, 'Needs attention'), (4, 'Cosmetic'), (5, 'Minor defect'), (6, 'To do')], validators=[DataRequired()])
    # issue_type = RadioField('Issue Type', choices=[('Critical', 'Severe', 'Needs attention', 'Cosmetic', 'Minor defect')], validators=[DataRequired()])
    issue_content = TextAreaField('What`s the problem', validators=[DataRequired()])
    file = FileField('Add file')
    submit = SubmitField('Add Issue')
