from flask import Blueprint, request, jsonify
from app.models import User, Ad
from app.extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils import upload_images

ads = Blueprint('ads', __name__)
@ads.route('/', methods=['GET'])
def get_ads():
    ads = Ad.query.all()
    ads_list = [ad.to_json() for ad in ads]
    return jsonify(ads_list), 200

@ads.route('/<ad_id>', methods=['GET'])
def get_ad(ad_id):
    ad = Ad.query.get_or_404(ad_id)
    return jsonify(ad.to_json()), 200

@ads.route('/category/<category_id>', methods=['GET'])
def get_ads_by_category(category_id):
    ads = Ad.query.filter_by(category_id=category_id).all()
    ads_list = [ad.to_json() for ad in ads]
    return jsonify(ads_list), 200

@ads.route('/create', methods=['POST'])
@jwt_required()
def create_ad():
    title = request.form.get('title')
    description = request.form.get('description')
    value = request.form.get('value')
    looking = request.form.get('looking')
    state = request.form.get('state')
    available = True
    category_id = request.form.get('category_id')

    images_url = upload_images(request)
    print(images_url)

    required_fiels = {
        'title': title,
        'description': description,
        'value': value,
        'looking': looking,
        'images_url': images_url,
        'state': state,
        'available': available,
        'category_id': category_id
    }

    mising_fields = [field for field, value in required_fiels.items() if not value]
    if mising_fields:
        return jsonify({'error': f'faltan datos para crear el anuncio: {", ".join(mising_fields)}'}), 400

    user_id = get_jwt_identity()

    ad = Ad(
        title=title,
        description=description,
        value=value,
        looking=looking,
        images_url=images_url,
        state=state,
        category_id=category_id,
        available=available,
        user_id=user_id
    )
    db.session.add(ad)
    db.session.commit()
    return jsonify({'message': 'Anuncio creado exitosamente', 'ad': ad.to_json()}), 201

@ads.route('/<ad_id>', methods=['PUT'])
@jwt_required()
def update_ad(ad_id):
    title = request.form.get('title')
    description = request.form.get('description')
    value = request.form.get('value')
    looking = request.form.get('looking')
    state = request.form.get('state')
    available = request.form.get('available')
    category_id = request.form.get('category_id')
    user_id = get_jwt_identity()
    ad = Ad.query.get_or_404(ad_id)
    images_url = upload_images(request)

    if ad.user_id != user_id:
        return jsonify({'error': 'No tienes permiso para actualizar este anuncio'}), 403
    
    ad.title = title
    ad.description = description
    ad.value = value
    ad.looking = looking
    ad.images_url = images_url
    ad.state = state
    ad.category_id = category_id
    ad.available = available
    db.session.commit()
    return jsonify({'message': 'Anuncio actualizado exitosamente', 'ad': ad.to_json()}), 200

