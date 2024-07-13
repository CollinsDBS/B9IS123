from flask import Blueprint

from app.controllers.auth_controller import auth_bp
from app.controllers.product_controller import product_bp
from app.controllers.appointment_controller import appointment_bp

bp = Blueprint('api', __name__)

bp.register_blueprint(auth_bp, url_prefix='/api/auth')
bp.register_blueprint(product_bp, url_prefix='/api')
bp.register_blueprint(appointment_bp, url_prefix='/api')
