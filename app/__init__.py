from flask import Flask
from config import Config
from app.extensions import db


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from app.auth.routes import auth_bp
    from app.main.routes import main_bp
    from app.api.routes import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    # Import models after initializing db
    from app import models

    with app.app_context():
        db.create_all()

    return app