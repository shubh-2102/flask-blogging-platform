from flask import render_template, abort
from app.blueprints.posts import posts_bp
from app.models import Post, Category, Tag

@posts_bp.route('/')
def list_posts():
    posts = Post.query.filter_by(published=True).order_by(Post.created_at.desc()).all()
    return render_template('posts/list.html', posts=posts)

@posts_bp.route('/<slug>')
def view_post(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    return render_template('posts/detail.html', post=post)
