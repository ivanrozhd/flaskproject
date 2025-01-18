from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('User-Email', validators=[DataRequired(), Email(), Length(min=10, max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('User-Email', validators=[DataRequired(), Email(), Length(min=10,max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Login')

class InterestForm(FlaskForm):
    hobby = StringField('Hobby', validators=[DataRequired(), Length(min=5, max=40)])
    description = StringField('Description', validators=[DataRequired(), Length(min=10, max=200)])
    submit = SubmitField('Add Interest')