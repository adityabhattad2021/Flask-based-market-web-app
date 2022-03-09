from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Length,EqualTo,DataRequired,ValidationError
from Flask_Project.models import User


class RegisterForm(FlaskForm):

    def validate_username(self,username_to_check):
        user=User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already taken, try a different one.")


    username = StringField(label='User Name:',validators=[Length(min=2,max=30),DataRequired()])
    email_address = StringField(label='Email:',validators=[DataRequired()])
    password1 = PasswordField(label='Password:',validators=[Length(min=6),DataRequired()])
    password2 = PasswordField(label='Confirm Password:',validators=[EqualTo('password1'),DataRequired()])
    submit = SubmitField(label='Click to Create Account ')


class LoginForm(FlaskForm):
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Log in')


class PurchaceItemForm(FlaskForm):
    submit = SubmitField(label='Buy it!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell it!')