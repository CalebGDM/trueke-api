from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required

users = Blueprint('users', __name__)

@users.route('/', methods=['GET'])
def get_all_users():
    try:
        users = User.query.all()
        users_list = [user.to_json() for user in users]
        return jsonify(users_list), 200
    except Exception as e:
        print("Error en /get-all:", e) 
        return jsonify({"error": str(e)}), 500

@users.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_json()), 200
    except Exception as e:
        print("Error en /get-user:", e) 
        return jsonify({"error": str(e)}), 500

@users.route('/register', methods=['POST'])
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
        print("Error en /register:", e) 
        return jsonify({"error": str(e)}), 500

@users.route('/login', methods=['POST'])
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

@users.route('/<user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    data = request.get_json()
    user = User.query.get_or_404(user_id)

    name = data.get('name', user.name)
    email = data.get('email', user.email)
    profile_picture_url = data.get('profile_picture_url', user.profile_picture_url)
    phone = data.get('phone', user.phone)
    address = data.get('address', user.address)
    rating = data.get('rating', user.rating)

    user.name = name
    user.email = email
    user.profile_picture_url = profile_picture_url
    user.phone = phone
    user.address = address
    user.rating = rating

    db.session.commit()

    return jsonify({"message": "Usuario actualizado exitosamente", "user": user.to_json()}), 200


