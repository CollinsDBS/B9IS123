from flask import Blueprint, request, jsonify
from app.models import User, Product, Appointment, Order
from app import db
from flask_jwt_extended import jwt_required
import os

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'message': 'User not found'}), 404

@admin_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.form
    file = request.files.get('image')
    image_url = None
    if file:
        image_url = os.path.join('uploads', file.filename)
        file.save(image_url)
    
    new_product = Product(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        category=data['category'],
        stock_quantity=data['stock_quantity'],
        image_url=image_url
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify(new_product.to_dict()), 201

@admin_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    product = Product.query.get(product_id)
    if product:
        data = request.form
        file = request.files.get('image')
        if file:
            image_url = os.path.join('uploads', file.filename)
            file.save(image_url)
            product.image_url = image_url
        
        product.name = data['name']
        product.description = data['description']
        product.price = data['price']
        product.category = data['category']
        product.stock_quantity = data['stock_quantity']
        db.session.commit()
        return jsonify(product.to_dict()), 200
    return jsonify({'message': 'Product not found'}), 404

@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted'}), 200
    return jsonify({'message': 'Product not found'}), 404

@admin_bp.route('/appointments', methods=['GET'])
@jwt_required()
def get_appointments():
    appointments = Appointment.query.all()
    return jsonify([appointment.to_dict() for appointment in appointments])

@admin_bp.route('/appointments/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        data = request.get_json()
        appointment.service_type = data['service_type']
        appointment.appointment_date = data['appointment_date']
        appointment.status = data['status']
        db.session.commit()
        return jsonify(appointment.to_dict()), 200
    return jsonify({'message': 'Appointment not found'}), 404

@admin_bp.route('/appointments/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    if appointment:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({'message': 'Appointment deleted'}), 200
    return jsonify({'message': 'Appointment not found'}), 404

@admin_bp.route('/orders', methods=['GET'])
@jwt_required()
def get_orders():
    orders = Order.query.all()
    return jsonify([order.to_dict() for order in orders])

@admin_bp.route('/orders/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    order = Order.query.get(order_id)
    if order:
        data = request.get_json()
        order.status = data['status']
        db.session.commit()
        return jsonify(order.to_dict()), 200
    return jsonify({'message': 'Order not found'}), 404

@admin_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    order = Order.query.get(order_id)
    if order:
        db.session.delete(order)
        db.session.commit()
        return jsonify({'message': 'Order deleted'}), 200
    return jsonify({'message': 'Order not found'}), 404
