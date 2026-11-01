import unittest
from app import create_app, db
from app.models import User


class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    # --- Registration Tests ---
    def test_register_page_loads(self):
        response = self.client.get('/auth/register')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create Your Account', response.data)

    def test_register_new_user(self):
        response = self.client.post('/auth/register', data={
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'StrongPass1',
            'confirm': 'StrongPass1',
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Account created', response.data)
        user = User.query.filter_by(username='newuser').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'newuser@example.com')

    def test_register_duplicate_email(self):
        u = User(username='existing', email='taken@example.com')
        u.set_password('Pass12345')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/auth/register', data={
            'username': 'newname',
            'email': 'taken@example.com',
            'password': 'Pass12345',
            'confirm': 'Pass12345',
        }, follow_redirects=True)
        self.assertIn(b'already exists', response.data)

    def test_register_duplicate_username(self):
        u = User(username='takenname', email='unique@example.com')
        u.set_password('Pass12345')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/auth/register', data={
            'username': 'takenname',
            'email': 'other@example.com',
            'password': 'Pass12345',
            'confirm': 'Pass12345',
        }, follow_redirects=True)
        self.assertIn(b'already taken', response.data)

    def test_register_password_mismatch(self):
        response = self.client.post('/auth/register', data={
            'username': 'mismatch',
            'email': 'mismatch@example.com',
            'password': 'Pass12345',
            'confirm': 'WrongPass1',
        }, follow_redirects=True)
        self.assertIn(b'Passwords must match', response.data)

    # --- Login Tests ---
    def test_login_page_loads(self):
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome Back', response.data)

    def test_login_valid_credentials(self):
        u = User(username='loginuser', email='login@example.com')
        u.set_password('MySecret99')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/auth/login', data={
            'email': 'login@example.com',
            'password': 'MySecret99',
            'remember': False,
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome back', response.data)

    def test_login_wrong_password(self):
        u = User(username='wrongpass', email='wrongpass@example.com')
        u.set_password('CorrectPass1')
        db.session.add(u)
        db.session.commit()

        response = self.client.post('/auth/login', data={
            'email': 'wrongpass@example.com',
            'password': 'WrongPass999',
        }, follow_redirects=True)
        self.assertIn(b'Invalid email or password', response.data)

    def test_login_nonexistent_email(self):
        response = self.client.post('/auth/login', data={
            'email': 'ghost@example.com',
            'password': 'SomePass123',
        }, follow_redirects=True)
        self.assertIn(b'Invalid email or password', response.data)

    # --- Profile Tests ---
    def test_profile_page_accessible(self):
        u = User(username='profileuser', email='profile@example.com')
        u.set_password('Pass12345')
        db.session.add(u)
        db.session.commit()

        response = self.client.get('/auth/profile/profileuser')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'profileuser', response.data)

    def test_profile_page_not_found(self):
        response = self.client.get('/auth/profile/nonexistentuser')
        self.assertEqual(response.status_code, 404)

    def test_edit_profile_requires_login(self):
        response = self.client.get('/auth/edit-profile', follow_redirects=True)
        self.assertIn(b'Sign In', response.data)

    # --- Logout Tests ---
    def test_logout_requires_login(self):
        response = self.client.get('/auth/logout', follow_redirects=True)
        # Redirected to login page since not authenticated
        self.assertIn(b'Sign In', response.data)


if __name__ == '__main__':
    unittest.main()
