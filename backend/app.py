from flask import Flask
from flask_cors import CORS
from backend.extensions import db, migrate
from backend.rutas.usuarios import usuarios_bp
from backend.rutas.search import search_bp
from backend.config import Config

def create_app():
    # Crea e inicializa la app Flask
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)


    db.init_app(app)       # base de datos
    migrate.init_app(app, db)  #  migraciones

    # Registra blueprints
    app.register_blueprint(usuarios_bp)
    app.register_blueprint(search_bp, url_prefix="/api")

    # Muestra rutas registradas en consola
    for rule in app.url_map.iter_rules():
        print(f"[RUTA REGISTRADA] {rule}")

    return app

if __name__ == '__main__':
    # Ejecuta en modo desarrollo
    app = create_app()
    app.run(debug=True)
