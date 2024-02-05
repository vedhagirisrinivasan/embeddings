from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from app.extensions import db
from app.api import api_bp


def create_app():
    app = Flask(__name__)
    JWTManager(app)

    app.config.from_object("config.Config")

    db.init_app(app)
    migrate = Migrate(app,db)
    migrate.init_app(app, db)

    app.register_blueprint(api_bp, url_prefix="/api")

    return app