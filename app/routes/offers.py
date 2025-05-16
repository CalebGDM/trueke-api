from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Offer
from app.extensions import db
from app.utils import upload_images

offers = Blueprint('offers', __name__)

@offers.route('/', methods=['GET'])
def get_offers():
    offers = Offer.query.all()
    offers_list = [offer.to_json() for offer in offers]
    return jsonify(offers_list), 200

@offers.route('/<offer_id>', methods=['GET'])
def get_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    return jsonify(offer.to_json()), 200

@offers.route('/ad/<ad_id>', methods=['GET'])
def get_offers_by_ad(ad_id):
    offers = Offer.query.filter_by(ad_id=ad_id).all()
    offers_list = [offer.to_json() for offer in offers]
    return jsonify(offers_list), 200

@offers.route('/user/<user_id>', methods=['GET'])
def get_offers_by_user(user_id):
    offers = Offer.query.filter_by(user_id=user_id).all()
    offers_list = [offer.to_json() for offer in offers]
    return jsonify(offers_list), 200

@offers.route('/create', methods=['POST'])
@jwt_required()
def create_offer():
    title = request.form.get('title')
    description = request.form.get('description')
    value = request.form.get('value')
    images_url = upload_images(request)
    state = request.form.get('state')
    category_id = request.form.get('category_id')
    ad_id = request.form.get('ad_id')

    user_id = get_jwt_identity()

    required_fields = {
        'title': title,
        'description': description,
        'value': value,
        'images_url': images_url,
        'state': state,
        'category_id': category_id
    }

    missing_fields = [field for field, value in required_fields.items() if not value]

    if missing_fields:
        return jsonify({'error': f'Missing fields to create the offer: {", ".join(missing_fields)}'}), 400
    offer = Offer(
        title=title,
        description=description,
        value=value,
        images_url=images_url,
        state=state,
        user_id=user_id,
        category_id=category_id,
        ad_id=ad_id
    )
    db.session.add(offer)
    db.session.commit()

    return jsonify({"message": "Oferta creada exitosamente", "offer": offer.to_json()}), 201

@offers.route('/<offer_id>', methods=['PUT'])
@jwt_required()
def update_offer(offer_id):
    data = request.get_json()
    offer = Offer.query.get_or_404(offer_id)

    title = data.get('title', offer.title)
    description = data.get('description', offer.description)
    value = data.get('value', offer.value)
    images_url = data.get('images_url', offer.images_url)
    state = data.get('state', offer.state)
    category_id = data.get('category_id', offer.category_id)

    offer.title = title
    offer.description = description
    offer.value = value
    offer.images_url = images_url
    offer.state = state
    offer.category_id = category_id
    db.session.commit()
    return jsonify({"message": "Oferta actualizada exitosamente", "offer": offer.to_json()}), 200

@offers.route('/<offer_id>', methods=['DELETE'])
@jwt_required()
def delete_offer(offer_id):
    offer = Offer.query.get_or_404(offer_id)
    db.session.delete(offer)
    db.session.commit()
    return jsonify({"message": "Oferta eliminada exitosamente"}), 200



