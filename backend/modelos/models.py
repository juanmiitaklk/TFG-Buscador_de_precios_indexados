from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask import current_app

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps(self.email, salt='email-confirm')

    @staticmethod
    def confirm_token(token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            email = s.loads(token, salt='email-confirm', max_age=expiration)
        except:
            return False
        return email

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "confirmed": self.confirmed
        }
