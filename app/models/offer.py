from uuid import uuid4
from app.extensions import db

class Offer(db.Model):
    __tablename__ = 'offers'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(120), unique=True, nullable=False)
    value = db.Column(db.Float(), nullable=False)
    images_url = db.Column(db.JSON, nullable=False)
    state = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    category_id = db.Column(db.String(36), db.ForeignKey('categories.id'), nullable=False)
    ad_id = db.Column(db.String(36), db.ForeignKey('ads.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, default=db.func.now())

    def __init__(self, title, description, value, images_url, state, category, user_id, category_id, ad_id):
        self.title = title
        self.description = description
        self.value = value
        self.images_url = images_url
        self.state = state
        self.category = category
        self.user_id = user_id
        self.category_id = category

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'value': self.value,
            'images_url': self.images_url,
            'state': self.state,
            'category': self.category,
            'user_id': self.user_id,
            'category_id': self.category_id,
            'ad_id': self.ad_id,
            'created_at': str(self.created_at)
        }