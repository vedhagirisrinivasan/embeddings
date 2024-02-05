from flask import Blueprint, request, jsonify
from app.api.auth.auth_controllers import signup_user, login_user

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    response, status_code = signup_user(data)
    return jsonify(response), status_code

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    response, status_code = login_user(data)
    return jsonify(response), status_code