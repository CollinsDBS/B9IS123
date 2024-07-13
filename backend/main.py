from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from config import Config
import logging
from logging.handlers import RotatingFileHandler
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    from app.controllers.auth_controller import auth_bp
    from app.controllers.appointment_controller import appointment_bp
    from app.controllers.product_controller import product_bp
    from app.controllers.order_controller import order_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(appointment_bp, url_prefix='/api')
    app.register_blueprint(product_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api')

    if not app.debug and not app.testing:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/flower_oasis.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Flower Oasis startup')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
