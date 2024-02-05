from datetime import datetime, timedelta

from flask import current_app
from flask_jwt_extended import create_access_token, create_refresh_token

from app.models.models import User


def generate_access_token(user_id, expires_in=None):
    if expires_in is None:
        expires_in = timedelta(hours=1)

    user = User.query.filter_by(uuid=user_id).first()
    token = create_access_token(
        identity=str(user_id),
        expires_delta=expires_in,
    )
    return token


def generate_refresh_token(user_id, expires_in=None):
    if expires_in is None:
        expires_in = timedelta(days=365)

    token = create_refresh_token(identity=str(user_id), expires_delta=expires_in)
    return token
