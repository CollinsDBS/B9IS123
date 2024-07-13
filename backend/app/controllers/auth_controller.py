import logging
import traceback
from flask import Blueprint, request, jsonify
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if not username or not email or not password:
            return jsonify({'message': 'Missing required fields'}), 400

        if User.query.filter_by(username=username).first() is not None:
            return jsonify({'message': 'Username already exists'}), 400

        new_user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            role='customer'  # Default role, change if needed
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        logger.error("Error occurred during registration: %s", e)
        logger.error(traceback.format_exc())  # Log the full traceback
        return jsonify({'message': 'Internal Server Error'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity={'id': user.id, 'username': user.username, 'role': user.role})
            return jsonify({'access_token': access_token}), 200

        return jsonify({'message': 'Invalid credentials'}), 401
    except Exception as e:
        logging.error(f"Error during login: {e}")
        logging.error(traceback.format_exc())  # Log the full traceback
        return jsonify({'message': 'Internal server error'}), 500
