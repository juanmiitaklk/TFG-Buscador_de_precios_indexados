from backend.extensions import db

class Usuario(db.Model):
        # Modelo de usuario para la base de datos
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    contraseña = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        # Devuelve el usuario como diccionario (sin contraseña)
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email
        }
