import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta')
    SQLALCHEMY_DATABASE_URI = 'sqlite:///db.sqlite3'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de correo (ejemplo con Gmail)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'tu_correo@gmail.com'
    MAIL_PASSWORD = 'tu_contraseña_de_aplicación'
