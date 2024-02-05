from app.extensions import db
from app.models.models import UserEmbeddings
from config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

connection_string = Config.SQLALCHEMY_DATABASE_URI


def get_embeddings(user_id):
    user_embeds = UserEmbeddings.query.filter_by(user_id=user_id).all()

    if user_embeds:
        collection_uuids = []
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        session = Session()

        for user_embed in user_embeds:
            collection_id = user_embed.embedding_id

            sql_query = text(
                "SELECT uuid FROM langchain_pg_embedding WHERE collection_id = :collection_id"
            )
            collection_uuid = session.execute(
                sql_query, {"collection_id": collection_id}
            ).scalar()
            session.close()

            if collection_uuid:
                collection_uuids.append(collection_uuid)

        return collection_uuids
    else:
        None
