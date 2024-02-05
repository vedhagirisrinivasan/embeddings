import os

import openai
from app.api.embed.embed_controllers import embed_files, prompting
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required

embed_bp = Blueprint("embed", __name__)


@embed_bp.route("/embedding", methods=["POST"])
@jwt_required()
def embeddings():
    data = request.get_json()
    response, status_code = embed_files(data)
    return jsonify(response), status_code


@embed_bp.route("/query", methods=["POST"])
@jwt_required()
def prompt():
    data = request.get_json()
    response, status_code = prompting(data)
    return jsonify(response), status_code
