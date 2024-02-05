import os


class Config:
    SECRET_KEY = "df3b31b89a5f0e7904b1220344900ab6"

    db_host = os.environ.get("DB_HOST")
    db_name = os.environ.get("DB_NAME")
    db_port = os.environ.get("DB_PORT")
    db_username = os.environ.get("DB_USERNAME")
    db_password = os.environ.get("DB_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"


