import unittest
from app import create_app, db
from app.models import User, Post, Category, Tag

class Week1TestCase(unittest.TestCase):
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

    def test_app_exists(self):
        self.assertFalse(self.app is None)

    def test_app_is_testing(self):
        self.assertTrue(self.app.config['TESTING'])

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Flask Blogging Platform', response.data)

    def test_about_page(self):
        response = self.client.get('/about')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'About the Flask Blogging Platform', response.data)

    def test_posts_page(self):
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'All Articles', response.data)

    def test_404_page(self):
        response = self.client.get('/nonexistent-page')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page Not Found', response.data)

    def test_user_password_hashing(self):
        u = User(username='testuser', email='test@example.com')
        u.set_password('mysecretpass')
        self.assertTrue(u.check_password('mysecretpass'))
        self.assertFalse(u.check_password('wrongpass'))
        self.assertNotEqual(u.password_hash, 'mysecretpass')

    def test_model_relationships(self):
        u = User(username='author1', email='author1@example.com')
        u.set_password('pass123')
        c = Category(name='Tech', slug='tech')
        t = Tag(name='Flask', slug='flask')
        db.session.add_all([u, c, t])
        db.session.commit()

        p = Post(
            title='Getting Started with Flask',
            slug='getting-started-with-flask',
            content='Flask is awesome!',
            author=u,
            category=c
        )
        p.tags.append(t)
        db.session.add(p)
        db.session.commit()

        self.assertEqual(p.author.username, 'author1')
        self.assertEqual(p.category.name, 'Tech')
        self.assertEqual(len(p.tags), 1)
        self.assertEqual(p.tags[0].name, 'Flask')

if __name__ == '__main__':
    unittest.main()
