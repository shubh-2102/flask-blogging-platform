from flask import render_template
from app.blueprints.main import main_bp
from app.models import Post, Category, Tag

@main_bp.route('/')
def index():
    posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).limit(6).all()
    categories = Category.query.all()
    tags = Tag.query.limit(10).all()
    return render_template('main/index.html', posts=posts, categories=categories, tags=tags)

@main_bp.route('/about')
def about():
    return render_template('main/about.html')
