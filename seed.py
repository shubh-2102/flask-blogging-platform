from app import create_app, db
from app.models import User, Post, Category, Tag, Comment

app = create_app('development')

def seed_database():
    with app.app_context():
        # Check if already seeded
        if User.query.first():
            print("Database already contains data.")
            return

        print("Seeding initial data...")

        # Create Demo Author
        author = User(
            username='flaskdev',
            email='dev@flaskblog.local',
            bio='Software engineer & Flask enthusiast building modern web applications.'
        )
        author.set_password('DevPassword123!')
        db.session.add(author)

        # Create Categories
        categories = [
            Category(name='Technology', slug='technology', description='Articles on software, web dev, and computing.'),
            Category(name='Tutorials', slug='tutorials', description='Step-by-step guides and walkthroughs.'),
            Category(name='Architecture', slug='architecture', description='System design and best practices.')
        ]
        db.session.add_all(categories)

        # Create Tags
        tags = [
            Tag(name='Python', slug='python'),
            Tag(name='Flask', slug='flask'),
            Tag(name='SQLAlchemy', slug='sqlalchemy'),
            Tag(name='WebDev', slug='webdev')
        ]
        db.session.add_all(tags)
        db.session.commit()

        # Create Sample Welcome Post
        post = Post(
            title='Welcome to the Flask Blogging Platform',
            slug='welcome-to-the-flask-blogging-platform',
            summary='An introduction to the Flask blogging platform built for the DIY Internship.',
            content='<p>Welcome to our new blogging platform! This project is structured using modern Flask standards including Application Factories, Blueprints, and SQLAlchemy ORM.</p><p>Stay tuned as we roll out user authentication, rich text editing, and comment threads in the upcoming weeks!</p>',
            author=author,
            category=categories[0]
        )
        post.tags.extend([tags[0], tags[1]])
        db.session.add(post)
        db.session.commit()

        # Add initial comment
        comment = Comment(
            body='Awesome architecture! Excited for Week 2 authentication features.',
            author=author,
            post=post
        )
        db.session.add(comment)
        db.session.commit()

        print("Database seeded successfully!")

if __name__ == '__main__':
    seed_database()
