from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        profile_picture_url = data.get('profile_picture_url')
        phone = data.get('phone')
        address = data.get('address')
        rating = data.get('rating')

        if not name or not email or not password:
            return jsonify({'error': 'faltan datos para el registror'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': "El email ya está registrado"}), 400

        if User.query.filter_by(name=name).first():
            return jsonify({'error': 'Ese nombre de usuario ya está registrado'}), 400

        user = User(name=name, email=email, password_hash=password, profile_picture_url=profile_picture_url,
                    phone=phone, address=address, rating=rating)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()
        return jsonify({'message': 'Usuario registrado exitosamente'}), 201
    except Exception as e:
        print("Error en /register:", e)  # 👈 esto imprime en la terminal
        return jsonify({"error": str(e)}), 500

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'faltan datos para el login'}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({'error': 'Credenciales inválidas'}), 401
    
    access_token = create_access_token(identity=user.id)

    return jsonify({'access_token': access_token}), 200
