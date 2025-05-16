from uuid import uuid4
from app.extensions import db


class Ad(db.Model):
    __tablename__ = 'ads'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.Float(), nullable=False)
    looking = db.Column(db.String(150), nullable=False)
    images_url = db.Column(db.JSON, nullable=False)
    state = db.Column(db.String(80), nullable=False)
    available = db.Column(db.Boolean(), default=True)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=False)
    offer_id = db.relationship('Offer', backref='ad', lazy=True)
    created_at = db.Column(db.TIMESTAMP, default=db.func.now())

    def __init__(self, title, description, value, looking, images_url, state, available, user_id, category_id):
        self.title = title
        self.description = description
        self.value = value
        self.looking = looking
        self.images_url = images_url
        self.state = state
        self.available = available
        self.user_id = user_id
        self.category_id = category_id 

   
    
    def to_json(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "value": self.value,
            "looking": self.looking,
            "images_url": self.images_url,
            "state": self.state,
            "available": self.available,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "offer_id": str(self.offer_id)  # Esto es lo que causa el problema
        }