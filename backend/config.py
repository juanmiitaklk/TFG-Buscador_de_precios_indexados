import os

class Config:
        # Clave secreta para sesiones y seguridad
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
        # Ruta de la base de datos SQLite
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../instance/db.sqlite3'
        # Desactiva seguimiento de cambios (mejora rendimiento)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
