import os

from dotenv import load_dotenv

load_dotenv()


class Config:
    """
    Base app config
    """

    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOADED_PHOTOS_DEST = "app/static/photos"

    # email config_options
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
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
