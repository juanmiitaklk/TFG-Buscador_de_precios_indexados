from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Instancia global de SQLAlchemy
db = SQLAlchemy()
# Instancia para manejar migraciones
migrate = Migrate()
