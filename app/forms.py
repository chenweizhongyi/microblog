from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField,PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    openid =StringField('openid',validators=[DataRequired()])
    remember_me = BooleanField('remember_me',default=False)

class SigninForm(FlaskForm):
    username = StringField('username',validators=[DataRequired()])
    email = StringField('email',validators=[DataRequired()])
    password1 = PasswordField('password',validators=[DataRequired()])
    password2 = PasswordField('password', validators=[DataRequired()])