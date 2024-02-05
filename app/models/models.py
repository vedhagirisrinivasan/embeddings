from sqlalchemy import text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import db
from datetime import datetime


class User(db.Model):
    __table_args__ = {"schema": "public"}
    __table_name__ = "users"

    uuid = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    first_name = db.Column(db.String(128), nullable=True)
    last_name = db.Column(db.String(128), nullable=True)
    email = db.Column(db.String(100), nullable=True, unique=True)
    password = db.Column(db.String(300), nullable=True, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class UserEmbeddings(db.Model):
    __table_args__ = {"schema": "public"}
    __table_name__ = "user_embeddings"

    uuid = db.Column(UUID(as_uuid=True), primary_key=True, server_default=text("uuid_generate_v4()"))
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(User.uuid))
    collection_name = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)






