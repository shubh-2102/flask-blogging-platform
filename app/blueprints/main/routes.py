from flask import render_template, request
from app.blueprints.main import main_bp
from app.models import Post, Category, Tag

@main_bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).paginate(page=page, per_page=6, error_out=False)
    categories = Category.query.order_by(Category.name).all()
    tags = Tag.query.order_by(Tag.name).limit(15).all()
    featured_post = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).first()
    return render_template('main/index.html', posts=posts, categories=categories, tags=tags, featured_post=featured_post)

@main_bp.route('/about')
def about():
    return render_template('main/about.html')

@main_bp.route('/health')
def health():
    return {'status': 'healthy', 'service': 'flask-blogging-platform'}, 200
