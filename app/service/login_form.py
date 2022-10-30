from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField, ValidationError
from wtforms.validators import Length, DataRequired


class LoginForm(FlaskForm):
    """
    登录表单格式
    """
    email_or_user = StringField(
        "Email or Username", validators=[DataRequired(), Length(1, 64)]
    )
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
