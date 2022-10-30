import random
import string
from flask import redirect, url_for, render_template, request
from flask_login import login_user

from app.service.register_form import RegistrationForm
from app.service.login_form import LoginForm
from app.service import auth
from app.model.user import User

num = string.ascii_letters+string.digits
auth.secret_key = "".join(random.sample(num, 10))


@auth.route('/register', methods=['GET', 'POST'])
def user_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        User(
            email=form.email.data,
            username=form.username.data,
            password=form.password.data,
        ).save()
        return redirect(url_for("auth.login"))
    return render_template("register.html", form=form)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_by_email = User.query.filter_by(email=form.email_or_username.data).first()
        user_by_name = User.query.filter_by(
            username=form.email_or_username.data
        ).first()
        if user_by_email is not None and user_by_email.verify_password(
            form.password.data
        ):
            login_user(user_by_email.seen())
            return redirect(request.args.get("next") or url_for("main.index"))
        if user_by_name is not None and user_by_name.verify_password(
            form.password.data
        ):
            login_user(user_by_name.seen())
            return redirect(request.args.get("next") or url_for("main.index"))
    return render_template("login.html", form=form)
