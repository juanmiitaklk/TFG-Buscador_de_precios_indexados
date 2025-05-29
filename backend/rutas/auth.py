from flask import Blueprint, request, jsonify, url_for
from flask_mail import Message
from flask_cors import cross_origin
from backend.modelos.models import db, User
from backend.extensions import mail

bp = Blueprint('auth', __name__) 

@bp.route('/status', methods=['GET'])
@cross_origin()
def status():
    return jsonify({'status': 'ok', 'message': 'Servidor activo'}), 200



@bp.route('/register', methods=['POST', 'OPTIONS'])
@cross_origin()
def register():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No se enviaron datos'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'El correo ya está registrado'}), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    token = user.generate_confirmation_token()
    confirm_url = url_for('auth.confirm_email', token=token, _external=True)
    msg = Message('Confirma tu cuenta', sender='noreply@example.com', recipients=[user.email])
    msg.body = f'Confirma tu cuenta aquí: {confirm_url}'
    print("CONFIRMATION URL:", confirm_url)
    mail.send(msg)

    return jsonify({'message': 'Usuario creado. Revisa tu correo para confirmar.'}), 201

@bp.route('/confirm/<token>', methods=['GET'])
@cross_origin()
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
