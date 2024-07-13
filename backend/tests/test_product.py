import unittest
from app import create_app, db
from app.models import Product

class ProductTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_add_product(self):
        response = self.client.post('/api/products', json={
            'name': 'Rose',
            'description': 'A beautiful flower',
            'price': 10.0,
            'category': 'Flower',
            'stock_quantity': 100
        })
        self.assertEqual(response.status_code, 201)

    def test_get_products(self):
        self.client.post('/api/products', json={
            'name': 'Rose',
            'description': 'A beautiful flower',
            'price': 10.0,
            'category': 'Flower',
            'stock_quantity': 100
        })
        response = self.client.get('/api/products')
        self.assertEqual(response.status_code, 200)
