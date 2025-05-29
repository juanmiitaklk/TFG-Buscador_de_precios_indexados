from flask import Flask
from flask_cors import CORS
from backend.extensions import db, migrate
from backend.rutas.usuarios import usuarios_bp
from backend.config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(usuarios_bp)

    for rule in app.url_map.iter_rules():
        print(f"[RUTA REGISTRADA] {rule}")


    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
