# app.py
from flask import Flask
from flask_cors import CORS
from backend.extensions import db, migrate, mail
from backend.rutas import auth, search 

def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.config.Config')

    # Habilita CORS
    CORS(app, supports_credentials=True)

    # Inicializa extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    # Registra blueprints
    app.register_blueprint(auth.bp, url_prefix='/api')
    app.register_blueprint(search.search_bp, url_prefix='/api') 

    return app
