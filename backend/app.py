from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from backend.extensions import db, migrate, mail
from backend.rutas import auth, search

import os

load_dotenv()

print("MAIL_USERNAME:", os.getenv("MAIL_USERNAME"))
print("MAIL_PASSWORD:", os.getenv("MAIL_PASSWORD")[:4] + "..." if os.getenv("MAIL_PASSWORD") else "No definida")
print("SECRET_KEY:", os.getenv("SECRET_KEY")[:4] + "..." if os.getenv("SECRET_KEY") else "No definida")

def create_app():
    app = Flask(__name__)
    app.config.from_object('backend.config.Config')

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)


    app.register_blueprint(auth.bp, url_prefix='/api')
    app.register_blueprint(search.search_bp, url_prefix='/api')

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
