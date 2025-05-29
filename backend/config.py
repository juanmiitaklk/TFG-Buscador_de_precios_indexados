import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
