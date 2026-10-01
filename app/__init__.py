from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_uploads import IMAGES, UploadSet, configure_uploads

from config import config_options

bootstrap = Bootstrap()
db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

photos = UploadSet("photos", IMAGES)

login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


def create_app(config_name="development"):
    app = Flask(__name__)

    app.config.from_object(config_options[config_name])

    bootstrap.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    configure_uploads(app, photos)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint

    app.register_blueprint(
        auth_blueprint,
        url_prefix="/authenticate",
    )

    return app
