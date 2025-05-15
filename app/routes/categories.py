from flask import Blueprint, request, jsonify
from app.models import Category
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

categories = Blueprint('categories', __name__)

@categories.route('/', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    categories_list = [category.to_json() for category in categories]
    return jsonify(categories_list), 200

@categories.route('/<category_id>', methods=['GET'])
def get_category(category_id):
    category = Category.query.get_or_404(category_id)
    return jsonify(category.to_json()), 200

@categories.route('/<category_id>/ads', methods=['GET'])
def get_ads_by_category(category_id):
    category = Category.query.get_or_404(category_id)
    ads = category.ads
    ads_list = [ad.to_json() for ad in ads]
    return jsonify(ads_list), 200

@categories.route('/create', methods=['POST'])
@jwt_required()
def create_category():
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'faltan datos para crear la categoria'}), 400

    category = Category(name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify({'message': 'Categoria creada exitosamente', 'category': category.to_json()}), 201

@categories.route('/<category_id>', methods=['PUT'])
@jwt_required()
def update_category(category_id):
    data = request.get_json()
    name = data.get('name')

    if not name:
        return jsonify({'error': 'faltan datos para actualizar la categoria'}), 400

    category = Category.query.get_or_404(category_id)
    category.name = name
    db.session.commit()
    return jsonify({'message': 'Categoria actualizada exitosamente', 'category': category.to_json()}), 200

@categories.route('/<category_id>', methods=['DELETE'])
@jwt_required()
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({'message': 'Categoria eliminada exitosamente'}), 200





