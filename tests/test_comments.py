import unittest
from app import create_app, db
from app.models import User, Post, Category, Comment
from app.blueprints.posts.forms import slugify


class CommentTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create author
        self.author = User(username='postauthor', email='author@test.com')
        self.author.set_password('Password123')

        # Create commenter
        self.commenter = User(username='commenter', email='commenter@test.com')
        self.commenter.set_password('Password123')

        # Create bystander
        self.bystander = User(username='bystander', email='bystander@test.com')
        self.bystander.set_password('Password123')

        # Create category & post
        self.cat = Category(name='Discussion', slug='discussion')
        db.session.add_all([self.author, self.commenter, self.bystander, self.cat])
        db.session.commit()

        self.post = Post(
            title='Sample Discussion Post',
            slug='sample-discussion-post',
            content='<p>Let us talk about software engineering.</p>',
            author=self.author,
            category=self.cat,
            published=True
        )
        db.session.add(self.post)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def _login(self, email='commenter@test.com', password='Password123'):
        return self.client.post('/auth/login', data={
            'email': email,
            'password': password
        }, follow_redirects=True)

    def test_anonymous_user_cannot_comment(self):
        resp = self.client.post(f'/posts/{self.post.slug}/comments', data={
            'body': 'This should fail because I am not logged in.'
        }, follow_redirects=True)
        self.assertIn(b'Sign In', resp.data)
        self.assertEqual(Comment.query.count(), 0)

    def test_authenticated_user_can_comment(self):
        self._login()
        resp = self.client.post(f'/posts/{self.post.slug}/comments', data={
            'body': 'Great article, thoroughly enjoyed reading it!'
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Your comment has been posted!', resp.data)

        comment = Comment.query.first()
        self.assertIsNotNone(comment)
        self.assertEqual(comment.body, 'Great article, thoroughly enjoyed reading it!')
        self.assertEqual(comment.author.username, 'commenter')
        self.assertEqual(comment.post.id, self.post.id)

    def test_comment_renders_on_post_page(self):
        comment = Comment(
            body='Awesome insights shared here.',
            author=self.commenter,
            post=self.post
        )
        db.session.add(comment)
        db.session.commit()

        resp = self.client.get(f'/posts/{self.post.slug}')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Awesome insights shared here.', resp.data)
        self.assertIn(b'commenter', resp.data)

    def test_comment_author_can_delete_comment(self):
        comment = Comment(
            body='I want to remove this remark.',
            author=self.commenter,
            post=self.post
        )
        db.session.add(comment)
        db.session.commit()

        self._login(email='commenter@test.com')
        resp = self.client.post(f'/posts/comments/{comment.id}/delete', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Comment removed successfully.', resp.data)
        self.assertIsNone(db.session.get(Comment, comment.id))

    def test_post_author_can_delete_any_comment(self):
        # Post author can moderate comments on their post
        comment = Comment(
            body='Inappropriate remark by someone else.',
            author=self.commenter,
            post=self.post
        )
        db.session.add(comment)
        db.session.commit()

        self._login(email='author@test.com')
        resp = self.client.post(f'/posts/comments/{comment.id}/delete', follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Comment removed successfully.', resp.data)
        self.assertIsNone(db.session.get(Comment, comment.id))

    def test_unauthorized_user_cannot_delete_comment(self):
        comment = Comment(
            body='Legitimate comment.',
            author=self.commenter,
            post=self.post
        )
        db.session.add(comment)
        db.session.commit()

        # Bystander attempts to delete
        self._login(email='bystander@test.com')
        resp = self.client.post(f'/posts/comments/{comment.id}/delete')
        self.assertEqual(resp.status_code, 403)
        self.assertIsNotNone(db.session.get(Comment, comment.id))

    def test_cascade_delete_comments_with_post(self):
        comment = Comment(
            body='Will be cascade deleted.',
            author=self.commenter,
            post=self.post
        )
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id

        db.session.delete(self.post)
        db.session.commit()

        self.assertIsNone(db.session.get(Comment, comment_id))


if __name__ == '__main__':
    unittest.main()
