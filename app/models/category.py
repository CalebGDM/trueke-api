from uuid import uuid4
from app.extensions import db

class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid4()))
    name = db.Column(db.String(100), nullable=False)
    ads = db.relationship('Ad', backref='category', lazy=True)
    created_at = db.Column(db.TIMESTAMP, default=db.func.now())

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': str(self.created_at)
        }