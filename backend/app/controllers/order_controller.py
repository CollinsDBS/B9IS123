import logging
import traceback
from datetime import datetime
from flask import Blueprint, request, jsonify
from app.models import Order, Product
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

order_bp = Blueprint('orders', __name__)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@order_bp.route('/orders', methods=['POST'])
@jwt_required()
def create_order():
    data = request.get_json()
    user_id = get_jwt_identity()['id']
    total_amount = data.get('total_amount')
    items = data.get('items')

    if not items or not total_amount:
        return jsonify({'message': 'Missing required fields'}), 400

    new_order = Order(
        user_id=user_id,
        order_date=datetime.utcnow(),
        total_amount=total_amount,
        items=items
    )
    db.session.add(new_order)
    db.session.commit()

    return jsonify({'message': 'Order created successfully'}), 201

@order_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    try:
        user_id = get_jwt_identity()['id']
        orders = Order.query.filter_by(user_id=user_id).all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        logger.error("Error occurred while fetching orders: %s", e)
        logger.error(traceback.format_exc())  # Log the full traceback
        return jsonify({'message': 'Internal Server Error'}), 500

@order_bp.route('/admin/orders', methods=['GET'])
@jwt_required()
def get_all_orders():
    try:
        orders = Order.query.all()
        return jsonify([order.to_dict() for order in orders]), 200
    except Exception as e:
        logger.error("Error occurred while fetching all orders: %s", e)
        logger.error(traceback.format_exc())  # Log the full traceback
        return jsonify({'message': 'Internal Server Error'}), 500
