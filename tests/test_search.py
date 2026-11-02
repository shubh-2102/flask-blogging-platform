import unittest
from app import create_app, db
from app.models import User, Post, Category, Tag


class SearchAndFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create user
        self.author = User(username='searchwriter', email='writer@test.com')
        self.author.set_password('Password123')

        # Create categories
        self.cat_python = Category(name='Python Development', slug='python-development')
        self.cat_web = Category(name='Web Design', slug='web-design')

        # Create tags
        self.tag_flask = Tag(name='Flask', slug='flask')
        self.tag_react = Tag(name='React', slug='react')
        self.tag_tutorial = Tag(name='Tutorial', slug='tutorial')

        db.session.add_all([
            self.author,
            self.cat_python, self.cat_web,
            self.tag_flask, self.tag_react, self.tag_tutorial
        ])
        db.session.commit()

        # Create sample posts
        self.post1 = Post(
            title='Getting Started with Flask and Blueprints',
            slug='getting-started-flask-blueprints',
            summary='An introduction to structuring scalable web apps with Flask.',
            content='<p>Flask provides blueprints to organize application components cleanly.</p>',
            author=self.author,
            category=self.cat_python,
            published=True
        )
        self.post1.tags.extend([self.tag_flask, self.tag_tutorial])

        self.post2 = Post(
            title='Modern Frontend Architecture with React',
            slug='modern-frontend-architecture-react',
            summary='How to build modular component hierarchies.',
            content='<p>React simplifies declarative UI state management.</p>',
            author=self.author,
            category=self.cat_web,
            published=True
        )
        self.post2.tags.extend([self.tag_react])

        self.post3 = Post(
            title='Advanced SQLAlchemy ORM Queries',
            slug='advanced-sqlalchemy-orm-queries',
            summary='Mastering joins, eager loading, and filtering.',
            content='<p>Deep dive into SQLAlchemy relationships and query expressions.</p>',
            author=self.author,
            category=self.cat_python,
            published=True
        )
        self.post3.tags.extend([self.tag_flask, self.tag_tutorial])

        self.draft = Post(
            title='Unpublished Secret Post',
            slug='unpublished-secret-post',
            summary='Secret draft not visible in search.',
            content='<p>Secret content with Flask keywords.</p>',
            author=self.author,
            category=self.cat_python,
            published=False
        )

        db.session.add_all([self.post1, self.post2, self.post3, self.draft])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_search_by_title(self):
        resp = self.client.get('/posts/?q=Blueprints')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Getting Started with Flask and Blueprints', resp.data)
        self.assertNotIn(b'Modern Frontend Architecture with React', resp.data)

    def test_search_by_content(self):
        resp = self.client.get('/posts/?q=declarative')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Modern Frontend Architecture with React', resp.data)
        self.assertNotIn(b'Getting Started with Flask and Blueprints', resp.data)

    def test_search_by_summary(self):
        resp = self.client.get('/posts/?q=Mastering')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Advanced SQLAlchemy ORM Queries', resp.data)

    def test_search_case_insensitive(self):
        resp = self.client.get('/posts/?q=flask')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Getting Started with Flask and Blueprints', resp.data)

    def test_search_no_matches(self):
        resp = self.client.get('/posts/?q=NonexistentQueryXYZ')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'No posts found', resp.data)
        self.assertIn(b'NonexistentQueryXYZ', resp.data)

    def test_search_excludes_drafts(self):
        resp = self.client.get('/posts/?q=Secret')
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(b'Unpublished Secret Post', resp.data)

    def test_filter_by_category(self):
        resp = self.client.get(f'/posts/?category={self.cat_web.slug}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Modern Frontend Architecture with React', resp.data)
        self.assertNotIn(b'Getting Started with Flask and Blueprints', resp.data)

    def test_filter_by_tag(self):
        resp = self.client.get(f'/posts/?tag={self.tag_react.slug}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Modern Frontend Architecture with React', resp.data)
        self.assertNotIn(b'Getting Started with Flask and Blueprints', resp.data)

    def test_combined_search_and_category_filter(self):
        # Search "Flask" in category "python-development"
        resp = self.client.get(f'/posts/?q=Flask&category={self.cat_python.slug}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Getting Started with Flask and Blueprints', resp.data)
        self.assertNotIn(b'Modern Frontend Architecture with React', resp.data)

    def test_combined_search_and_category_no_match(self):
        # Search "React" in category "python-development" -> 0 matches
        resp = self.client.get(f'/posts/?q=React&category={self.cat_python.slug}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'No posts found', resp.data)


if __name__ == '__main__':
    unittest.main()
