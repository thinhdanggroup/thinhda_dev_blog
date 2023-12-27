import os
import unittest

from testcontainers.postgres import PostgresContainer


class APITestCase(unittest.TestCase):
    container = None

    @classmethod
    def setUpClass(cls):
        cls.container = PostgresContainer("postgres:9.5")
        cls.container.start()
        os.environ["SQLALCHEMY_DATABASE_URI"] = cls.container.get_connection_url()
        from payment_testcontainers.app import app, db
        cls.app = app
        cls.db = db

    def setUp(self):
        with self.app.app_context():
            self.db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        with self.app.app_context():
            self.db.session.remove()
            self.db.drop_all()

    def test_create_payment(self):
        response = self.client.post('/payments', json={'amount': 100.0, 'currency': 'USD'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.get_json())

        response = self.client.get(f"/payments/{response.get_json()['id']}")
        self.assertEqual(response.status_code, 200)
        payment = response.get_json()
        self.assertEqual(payment['amount'], 100.0)
        self.assertEqual(payment['currency'], "USD")
        self.assertEqual(payment['status'], "pending")
