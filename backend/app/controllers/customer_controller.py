from flask import Blueprint, request, jsonify
from app.models import Product, Appointment, Order, User, Cart
from app import db
from flask_jwt_extended import jwt_required, get_jwt_identity
import json

customer_bp = Blueprint('customer', __name__)

@customer_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products])

@customer_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return jsonify(product.to_dict()), 200
    return jsonify({'message': 'Product not found'}), 404

@customer_bp.route('/appointments', methods=['POST'])
@jwt_required()
def book_appointment():
    user_id = get_jwt_identity()['id']
    data = request.get_json()
    new_appointment = Appointment(
        user_id=user_id,
        service_type=data['service_type'],
        appointment_date=data['appointment_date']
    )
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify(new_appointment.to_dict()), 201

@customer_bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    user_id = get_jwt_identity()['id']
    appointments = Appointment.query.filter_by(user_id=user_id).all()
    return jsonify([appointment.to_dict() for appointment in appointments])

@customer_bp.route('/cart', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()['id']
    data = request.get_json()
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        cart = Cart(user_id=user_id, items=json.dumps([]), total_amount=0)
        db.session.add(cart)
        db.session.commit()
    
    items = json.loads(cart.items)
    items.append(data)
    cart.items = json.dumps(items)
    cart.total_amount += data['price']
    db.session.commit()
    return jsonify(cart.to_dict()), 201

@customer_bp.route('/cart', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()['id']
    cart = Cart.query.filter_by(user_id=user_id).first()
    if cart:
        return jsonify(cart.to_dict()), 200
    return jsonify({'message': 'Cart not found'}), 404

@customer_bp.route('/orders', methods=['POST'])
@jwt_required()
def place_order():
    user_id = get_jwt_identity()['id']
    cart = Cart.query.filter_by(user_id=user_id).first()
    if not cart:
        return jsonify({'message': 'Cart is empty'}), 400
    
    new_order = Order(
        user_id=user_id,
        total_amount=cart.total_amount,
        items=cart.items
    )
    db.session.add(new_order)
    db.session.commit()
    
    # Clear the cart
    cart.items = json.dumps([])
    cart.total_amount = 0
    db.session.commit()
    
    return jsonify(new_order.to_dict()), 201

@customer_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()['id']
    orders = Order.query.filter_by(user_id=user_id).all()
    return jsonify([order.to_dict() for order in orders])
