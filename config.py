import os

from dotenv import load_dotenv

load_dotenv()

database_url = os.getenv("DATABASE_URL")

if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace(
        "postgres://",
        "postgresql://",
        1,
    )


class Config:
    """
    Base app config
    """

    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADED_PHOTOS_DEST = "app/static/photos"

    # email config_options
    MAIL_SERVER = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.getenv("MAIL_PORT", "587"))
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    SENDER_EMAIL = os.getenv("MAIL_USERNAME")
    SUBJECT_PREFIX = "ThyVoice"


class DevConfig(Config):
    """
    development configuration
    """

    DEBUG = True


class ProdConfig(Config):
    """
    production configuration
    """

    DEBUG = False


config_options = {
    "development": DevConfig,
    "production": ProdConfig,
}
