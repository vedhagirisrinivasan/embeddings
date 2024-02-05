from app.utils.status import status
from flask_jwt_extended import verify_jwt_in_request
from validate_email_address import validate_email
from app.models.models import User
from werkzeug.security import check_password_hash, generate_password_hash
from app.utils.authentication import (generate_access_token,
                                      generate_refresh_token)
from app.extensions import db


def signup_user(data):
    email = data.get("email")
    first_name = data.get("first_name")
    last_name = data.get("last_name")
    password = data.get("password")

    if not validate_email(email):
            return (
                status(
                    status=True, body=None, message="Enter valid email", error=None
                ),
                400,
            )
    user = User(first_name=first_name, last_name=last_name, email=email,password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    user_details = User.query.filter_by(email=email).first()
    access_token = generate_access_token(user_details.uuid)
    refresh_token = generate_refresh_token(user_details.uuid)

    body =  {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {
            "email": email,
            "first_name": first_name,
            "last_name":  last_name,
            "id": user_details.uuid
        }
    }
    data = (status(status=True, body=body, message="USER ADDED", error=None), 200)

    return data, 200



    
def login_user(data):
    email = data.get("email")
    password = data.get("password")
    user = User.query.filter_by(email=email).first()
    if not user:
         return (status(status=False, body=None, message="USER NOT EXISTS", error=None), 400)
    if user and check_password_hash(user.password, password):
        user_details = User.query.filter_by(email=email).first()
        email = user_details.email
        first_name = user_details.first_name
        last_name = user_details.last_name
        access_token = generate_access_token(user_details.uuid)
        refresh_token = generate_refresh_token(user_details.uuid)

        body = {
            "accessToken": access_token,
            "refreshToken": refresh_token,
            "user": {
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "id": user_details.uuid,
            },
        }
        return (
            status(status=True, body=body, message="LOGGED SUCCESSFULLY", error=None),
            200,
        )
    else:
        return (
            status(status=False, body=None, message="INVALID CRDENTIALS", error=None),
            401,
        )
