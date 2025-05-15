from uuid import uuid4
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    profile_picture_url = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(400), nullable=False)
    rating = db.Column(db.Float(), nullable=False)
    ads = db.relationship('Ad', backref='user', lazy=True)
    created_at = db.Column(db.TIMESTAMP, default=db.func.now())

    def __init__(self, name, email, password_hash, profile_picture_url, phone, address, rating):
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.profile_picture_url = profile_picture_url
        self.phone = phone
        self.address = address
        self.rating = rating

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'profile_picture_url': self.profile_picture_url,
            'phone': self.phone,
            'address': self.address,
            'rating': self.rating,
            'created_at': str(self.created_at)
        }