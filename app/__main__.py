from flask_migrate import Migrate
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import Config
from app.routes import users, ads, categories, uploads, offers
from app.extensions import jwt
from app.extensions import db
from app.extensions import migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(users, url_prefix='/users')
    app.register_blueprint(ads, url_prefix='/ads')
    app.register_blueprint(offers, url_prefix='/offers')    
    app.register_blueprint(categories, url_prefix='/categories')
    app.register_blueprint(uploads, url_prefix='/uploads')

    return app


