import os


class Config:
    SECRET_KEY = "df3b31b89a5f0e7904b1220344900ab6"

    db_host = os.environ.get("db_host")
    db_name = os.environ.get("db_name")
    db_port = os.environ.get("db_port")
    db_username = os.environ.get("db_username")
    db_password = os.environ.get("db_password")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}"


