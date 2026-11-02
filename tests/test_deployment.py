import os
import unittest
from app import create_app
from app.config import config_by_name, ProductionConfig, TestingConfig, DevelopmentConfig


class DeploymentAndTestingTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_health_check_endpoint(self):
        """Test healthcheck endpoint used by Docker and container orchestrators."""
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        json_data = response.get_json()
        self.assertIsNotNone(json_data)
        self.assertEqual(json_data.get('status'), 'healthy')
        self.assertEqual(json_data.get('service'), 'flask-blogging-platform')

    def test_testing_configuration(self):
        """Ensure testing environment is properly isolated."""
        self.assertTrue(self.app.config['TESTING'])
        self.assertFalse(self.app.config['WTF_CSRF_ENABLED'])
        self.assertEqual(self.app.config['SQLALCHEMY_DATABASE_URI'], 'sqlite:///:memory:')

    def test_production_configuration(self):
        """Ensure production environment enforces secure defaults."""
        prod_app = create_app('production')
        self.assertFalse(prod_app.config['DEBUG'])
        self.assertFalse(prod_app.config['TESTING'])

    def test_development_configuration(self):
        """Ensure development environment enables debug mode."""
        dev_app = create_app('development')
        self.assertTrue(dev_app.config['DEBUG'])

    def test_wsgi_entrypoint_import(self):
        """Ensure wsgi.py is importable by Gunicorn without error."""
        import wsgi
        self.assertIsNotNone(wsgi.app)


if __name__ == '__main__':
    unittest.main()
