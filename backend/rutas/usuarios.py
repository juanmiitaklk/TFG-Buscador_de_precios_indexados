from flask import Blueprint, request, jsonify
from backend.modelos.models import db, Usuario

# Blueprint
usuarios_bp = Blueprint('usuarios', __name__, url_prefix='/api')

@usuarios_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    # Registra un nuevo usuario
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    contraseña = data.get('contraseña')

    if not all([nombre, email, contraseña]):
        return jsonify({"error": "Faltan datos"}), 400

    if Usuario.query.filter_by(email=email).first():
        return jsonify({"error": "El correo ya está registrado"}), 400

    nuevo_usuario = Usuario(nombre=nombre, email=email, contraseña=contraseña)
    db.session.add(nuevo_usuario)
    db.session.commit()

    return jsonify({"mensaje": "Usuario registrado exitosamente"}), 201

@usuarios_bp.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    # Lista todos los usuarios
    usuarios = Usuario.query.all()
    return jsonify([usuario.to_dict() for usuario in usuarios])

@usuarios_bp.route('/login', methods=['POST'])
def login():
    # Devuelve usuario por email sin validar la contraseña
    data = request.get_json()
    email = data.get('email')

    if not email:
        return jsonify({"error": "Falta el email"}), 400

    usuario = Usuario.query.filter_by(email=email).first()
    if not usuario:
        return jsonify({"error": "Correo no registrado"}), 404

    return jsonify(usuario.to_dict()), 200

@usuarios_bp.route('/usuarios/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    # Actualiza los datos de un usuario
    data = request.get_json()
    usuario = Usuario.query.get_or_404(id)

    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.email = data.get('email', usuario.email)
    usuario.contraseña = data.get('contraseña', usuario.contraseña)

    db.session.commit()
    return jsonify({"mensaje": "Usuario actualizado", "usuario": usuario.to_dict()})

@usuarios_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    # Elimina un usuario por ID
    usuario = Usuario.query.get_or_404(id)
    db.session.delete(usuario)
    db.session.commit()
    return jsonify({"mensaje": "Usuario eliminado"})
