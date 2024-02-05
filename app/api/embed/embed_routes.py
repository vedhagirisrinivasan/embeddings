from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.api.embed.embed_controllers import embed_files, prompting
import os
import openai

embed_bp = Blueprint("embed", __name__) 

openai.api_key  = os.getenv('OPENAI_API_KEY')

@embed_bp.route("/embedding",methods=["POST"])
@jwt_required()
def embeddings():
    data = request.get_json()
    response, status_code = embed_files(data)
    return jsonify(response), status_code

@embed_bp.route("/query",methods=["POST"])
@jwt_required()
def prompt():
    data = request.get_json()
    response, status_code = prompting(data)
    return jsonify(response), status_code