# python -m unittest discover tests

import unittest
from flask import Flask
from flask_testing import TestCase
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from models import Services

class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_services_api(self):
        response = self.client.get('/api/services')
        data = response.get_json()
        self.assertIn('services', data)

    def test_search_endpoint(self):
        response = self.client.get('/search?title=12')
        self.assert200(response)

    def test_specialists_endpoint(self):
        response = self.client.get('/specialists')
        self.assert200(response)

    def test_reviews_endpoint(self):
        response = self.client.get('/reviews')
        self.assert200(response)

def test_auth_endpoint(self):
    response = self.client.post('/auth', data=dict(email='example@example.com', password='password'))
    self.assert200(response)
