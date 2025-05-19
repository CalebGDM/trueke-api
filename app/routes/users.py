from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db
from flask_jwt_extended import create_access_token, jwt_required
from datetime import datetime
from app.utils import upload_image
from flask_restx import Namespace, Resource, fields

users = Blueprint('users', __name__)
users_ns = Namespace('users', description='User related operations')
user_model = users_ns.model('User', {
    'id': fields.String(readOnly=True, description='The unique identifier of a user'),
    'name': fields.String(required=True, description='The name of the user'),
    'email': fields.String(required=True, description='The email of the user'),
    'profile_picture_url': fields.String(description='The profile picture URL of the user'),
    'phone': fields.String(description='The phone number of the user'),
    'address': fields.String(description='The address of the user'),
    'rating': fields.Float(description='The rating of the user')
})

@users_ns.route('/')
class UserList(Resource):
    @users_ns.doc('list_users')
    @users_ns.marshal_list_with(user_model)
    def get(self):
        """List all users"""
        try:
            users = User.query.all()
            return [user.to_json() for user in users], 200
        except Exception as e:
            print("Error en /get-all:", e) 
            return {'error': str(e)}, 500
        
@users_ns.route('/<int:user_id>')
class UserDetail(Resource):
    @users_ns.doc('get_user')
    @users_ns.marshal_with(user_model)
    def get(self, user_id):
        """Get a user by ID"""
        try:
            user = User.query.get_or_404(user_id)
            return user.to_json(), 200
        except Exception as e:
            print("Error en /get-user:", e) 
            return {'error': str(e)}, 500
        
@users_ns.route('/register')
class UserRegister(Resource):
    @users_ns.doc('register_user')
    @users_ns.expect(user_model)
    def post(self):
        """Register a new user"""
        try:
            data = request.get_json()
            name = data.get('name')
            email = data.get('email')
            password = data.get('password')
            phone = data.get('phone')
            address = data.get('address')

            # Subir las imágenes
            profile_picture_url = upload_image(request)

            if not profile_picture_url:
                return {'error': 'No se pudo subir la imagen'}, 400

            if not name or not email or not password:
                return {'error': 'faltan datos para el registror'}, 400

            if User.query.filter_by(email=email).first():
                return {'error': "El email ya está registrado"}, 400

            if User.query.filter_by(name=name).first():
                return {'error': 'Ese nombre de usuario ya está registrado'}, 400

            user = User(name=name, email=email, password_hash=password, profile_picture_url=profile_picture_url,
                        phone=phone, address=address, rating=0)
            user.set_password(password)

            db.session.add(user)
            db.session.commit()
            return {'message': 'Usuario registrado exitosamente'}, 201
        except Exception as e:
            print("Error en /register:", e) 
            return {'error': str(e)}, 500

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
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')
        address = request.form.get('address')

        # Subir las imágenes
        
        profile_picture_url = upload_image(request)

        if not profile_picture_url:
            return jsonify({'error': 'No se pudo subir la imagen'}), 400

        if not name or not email or not password:
            return jsonify({'error': 'faltan datos para el registror'}), 400

        if User.query.filter_by(email=email).first():
            return jsonify({'error': "El email ya está registrado"}), 400

        if User.query.filter_by(name=name).first():
            return jsonify({'error': 'Ese nombre de usuario ya está registrado'}), 400

        user = User(name=name, email=email, password_hash=password, profile_picture_url=profile_picture_url,
                    phone=phone, address=address, rating=0)
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
  
    user = User.query.get_or_404(user_id)

    name = request.form.get('name', user.name)
    email = request.form.get('email', user.email)
 
    phone = request.form.get('phone', user.phone)
    address = request.form.get('address', user.address)

    profile_picture_url = upload_image(request)

    user.name = name
    user.email = email
    user.profile_picture_url = profile_picture_url
    user.phone = phone
    user.address = address


    db.session.commit()

    return jsonify({"message": "Usuario actualizado exitosamente", "user": user.to_json()}), 200


