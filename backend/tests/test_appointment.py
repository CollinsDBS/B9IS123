import unittest
from app import create_app, db
from app.models import Appointment, User

class AppointmentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()
            self.client.post('/api/auth/register', json={
                'username': 'testuser',
                'email': 'testuser@example.com',
                'password': 'password'
            })
            response = self.client.post('/api/auth/login', json={
                'username': 'testuser',
                'password': 'password'
            })
            self.token = response.json['access_token']

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_book_appointment(self):
        response = self.client.post('/api/appointments', json={
            'service_type': 'Landscaping',
            'appointment_date': '2024-07-15T10:00:00'
        }, headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 201)

    def test_get_appointments(self):
        self.client.post('/api/appointments', json={
            'service_type': 'Landscaping',
            'appointment_date': '2024-07-15T10:00:00'
        }, headers={'Authorization': f'Bearer {self.token}'})
        response = self.client.get('/api/appointments', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
