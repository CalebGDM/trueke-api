from flask_migrate import Migrate

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from app.config import Config
from app.routes import auth
from app.extensions import jwt
from app.extensions import db
from app.extensions import migrate

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(auth, url_prefix='/auth')

    return app


