from flask import Blueprint, request, jsonify, url_for
from backend.modelos.models import db, User
from flask_mail import Message
from backend.extensions import mail
from flask import current_app

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El correo ya está registrado'}), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    token = user.generate_confirmation_token()
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    msg = Message('Confirma tu cuenta', sender='tu-correo@ejemplo.com', recipients=[user.email])
    msg.body = f'Confirma tu cuenta aquí: {confirm_url}'
    mail.send(msg)

    return jsonify({'message': 'Usuario creado. Revisa tu correo para confirmar.'}), 201

@bp.route('/confirm/<token>')
def confirm_email(token):
    email = User.confirm_token(token)
    if not email:
        return jsonify({'error': 'Token inválido o expirado.'}), 400

    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        return jsonify({'message': 'Cuenta ya confirmada.'}), 200
    user.confirmed = True
    db.session.commit()
    return jsonify({'message': 'Cuenta confirmada.'}), 200

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()

    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Credenciales incorrectas'}), 401
    if not user.confirmed:
        return jsonify({'error': 'Cuenta no confirmada'}), 403

    return jsonify({'message': 'Login exitoso', 'user': user.to_dict()}), 200

@bp.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.username = data.get('username', user.username)
    if 'password' in data:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify({'message': 'Usuario actualizado', 'user': user.to_dict()}), 200

@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Usuario eliminado'}), 200
