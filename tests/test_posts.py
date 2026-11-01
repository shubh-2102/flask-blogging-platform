import unittest
from app import create_app, db
from app.models import User, Post, Category, Tag
from app.blueprints.posts.forms import slugify


class SlugifyTestCase(unittest.TestCase):
    def test_basic_slug(self):
        self.assertEqual(slugify('Hello World'), 'hello-world')

    def test_special_chars(self):
        self.assertEqual(slugify('Flask & Python!'), 'flask-python')

    def test_multiple_spaces(self):
        self.assertEqual(slugify('  My   Post Title  '), 'my-post-title')


class PostCRUDTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create test user and category
        self.user = User(username='author', email='author@test.com')
        self.user.set_password('Password99')
        self.cat = Category(name='Tech', slug='tech')
        db.session.add_all([self.user, self.cat])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def _login(self):
        self.client.post('/auth/login', data={
            'email': 'author@test.com',
            'password': 'Password99',
        }, follow_redirects=True)

    def _create_post(self, title='Test Post', content='<p>Hello</p>'):
        return Post(
            title=title,
            slug=slugify(title),
            content=content,
            author=self.user,
            published=True
        )

    # --- List Posts ---
    def test_list_posts_page_loads(self):
        resp = self.client.get('/posts/')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'All Articles', resp.data)

    def test_list_posts_by_category(self):
        post = self._create_post('Tech Post')
        post.category = self.cat
        db.session.add(post)
        db.session.commit()

        resp = self.client.get('/posts/?category=tech')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Tech Post', resp.data)

    def test_list_posts_invalid_category_404(self):
        resp = self.client.get('/posts/?category=nonexistent')
        self.assertEqual(resp.status_code, 404)

    # --- View Post ---
    def test_view_post(self):
        post = self._create_post('Readable Post')
        db.session.add(post)
        db.session.commit()

        resp = self.client.get(f'/posts/{post.slug}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Readable Post', resp.data)

    def test_view_nonexistent_post_404(self):
        resp = self.client.get('/posts/this-does-not-exist')
        self.assertEqual(resp.status_code, 404)

    # --- Create Post ---
    def test_create_post_requires_login(self):
        resp = self.client.get('/posts/create', follow_redirects=True)
        self.assertIn(b'Welcome Back', resp.data)

    def test_create_post_authenticated(self):
        self._login()
        resp = self.client.get('/posts/create')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Write a New Post', resp.data)

    def test_create_post_submit(self):
        self._login()
        resp = self.client.post('/posts/create', data={
            'title': 'My First Post',
            'content': '<p>Hello World</p>',
            'summary': 'A short summary',
            'category_id': 0,
            'tags': 'Flask, Python',
            'published': True,
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'My First Post', resp.data)
        post = Post.query.filter_by(slug='my-first-post').first()
        self.assertIsNotNone(post)
        self.assertEqual(len(post.tags), 2)

    # --- Edit Post ---
    def test_edit_post_only_author(self):
        post = self._create_post('Author Only')
        db.session.add(post)
        db.session.commit()

        # Another user
        other = User(username='hacker', email='hacker@test.com')
        other.set_password('Password99')
        db.session.add(other)
        db.session.commit()

        self.client.post('/auth/login', data={
            'email': 'hacker@test.com', 'password': 'Password99'
        }, follow_redirects=True)

        resp = self.client.get(f'/posts/{post.slug}/edit')
        self.assertEqual(resp.status_code, 403)

    # --- Delete Post ---
    def test_delete_post(self):
        self._login()
        post = self._create_post('Delete Me')
        db.session.add(post)
        db.session.commit()
        slug = post.slug

        resp = self.client.post(f'/posts/{slug}/delete', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIsNone(Post.query.filter_by(slug=slug).first())

    def test_delete_post_only_author(self):
        post = self._create_post('Protected')
        db.session.add(post)
        db.session.commit()

        other = User(username='intruder', email='intruder@test.com')
        other.set_password('Password99')
        db.session.add(other)
        db.session.commit()

        self.client.post('/auth/login', data={
            'email': 'intruder@test.com', 'password': 'Password99'
        }, follow_redirects=True)

        resp = self.client.post(f'/posts/{post.slug}/delete', follow_redirects=True)
        self.assertEqual(resp.status_code, 403)


if __name__ == '__main__':
    unittest.main()
