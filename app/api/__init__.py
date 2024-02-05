from flask import Blueprint

api_bp = Blueprint("api", __name__)

from app.api.auth import auth_routes
from app.api.embed import embed_routes


api_bp.register_blueprint(auth_routes.auth_bp, url_prefix="/auth")
api_bp.register_blueprint(embed_routes.embed_bp, url_prefix="/embed")

