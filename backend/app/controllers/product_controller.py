from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Product
from app import db

product_bp = Blueprint('products', __name__)

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    category = data.get('category')
    stock_quantity = data.get('stock_quantity')
    image_url = data.get('image_url')

    if not all([name, description, price, category, stock_quantity]):
        return jsonify({'message': 'Missing required fields'}), 400

    new_product = Product(
        name=name,
        description=description,
        price=price,
        category=category,
        stock_quantity=stock_quantity,
        image_url=image_url
    )
    db.session.add(new_product)
    db.session.commit()

    return jsonify({'message': 'Product added successfully'}), 201

@product_bp.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.to_dict() for product in products]), 200

@product_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict()), 200

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    product = Product.query.get_or_404(product_id)
    data = request.get_json()

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.category = data.get('category', product.category)
    product.stock_quantity = data.get('stock_quantity', product.stock_quantity)
    product.image_url = data.get('image_url', product.image_url)

    db.session.commit()
    return jsonify({'message': 'Product updated successfully'}), 200

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200
