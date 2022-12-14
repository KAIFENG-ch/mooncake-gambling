import re
import datetime

from sqlalchemy.orm import synonym
from flask import Flask, url_for
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app.model.BaseModel import BaseModel, check_length
from app import db, login_manager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ''

EMAIL_REGEX = re.compile(r"^\S+@\S+\.\S+$")
USERNAME_REGEX = re.compile(r"^\S+$")


class User(db.Model, UserMixin, BaseModel):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    _username = db.Column("username", db.String(64), unique=True)
    _email = db.Column("email", db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        if self.is_admin:
            return f"<Admin {self.username}>"
        return f"<User {self.username}>"

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username):
        is_valid_length = check_length(username, 64)
        if not is_valid_length or not bool(USERNAME_REGEX.match(username)):
            raise ValueError(f"{username} is not a valid username")
        self._username = username

    username = synonym("_username", descriptor=username)

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, email):
        if not check_length(email, 64) or not bool(EMAIL_REGEX.match(email)):
            raise ValueError(f"{email} is not a valid email address")
        self._email = email

    email = synonym("_email", descriptor=email)

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password):
        if not bool(password):
            raise ValueError("no password given")

        hashed_password = generate_password_hash(password)
        if not check_length(hashed_password, 128):
            raise ValueError("not a valid password, hash is too long")
        self.password_hash = hashed_password

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def seen(self):
        self.last_seen = datetime.utcnow()
        return self.save()

    def to_dict(self):
        return {
            "username": self.username,
            "user_url": url_for("api.get_user", username=self.username, _external=True),
            "member_since": self.member_since,
        }

    def promote_to_admin(self):
        self.is_admin = True
        return self.save()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
