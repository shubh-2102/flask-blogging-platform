from flask import render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app.blueprints.posts import posts_bp
from app.blueprints.posts.forms import PostForm, CommentForm, slugify
from app.extensions import db
from app.models.post import Post, Category, Tag
from app.models.comment import Comment


def _get_or_create_tag(name: str) -> Tag:
    """Return an existing Tag or create a new one."""
    slug = slugify(name)
    tag = Tag.query.filter_by(slug=slug).first()
    if not tag:
        tag = Tag(name=name.strip(), slug=slug)
        db.session.add(tag)
    return tag


def _populate_category_choices(form):
    """Fill SelectField with current categories."""
    choices = [(0, '— No Category —')]
    choices += [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    form.category_id.choices = choices


@posts_bp.route('/')
def list_posts():
    category_slug = request.args.get('category')
    tag_slug = request.args.get('tag')
    page = request.args.get('page', 1, type=int)

    query = Post.query.filter_by(published=True)

    if category_slug:
        cat = Category.query.filter_by(slug=category_slug).first_or_404()
        query = query.filter_by(category_id=cat.id)
    else:
        cat = None

    if tag_slug:
        tag = Tag.query.filter_by(slug=tag_slug).first_or_404()
        query = query.filter(Post.tags.contains(tag))
    else:
        tag = None

    posts = query.order_by(Post.created_at.desc()).paginate(page=page, per_page=9, error_out=False)
    categories = Category.query.order_by(Category.name).all()
    tags = Tag.query.order_by(Tag.name).limit(20).all()

    return render_template(
        'posts/list.html',
        posts=posts, categories=categories, tags=tags,
        active_category=cat, active_tag=tag
    )


@posts_bp.route('/<slug>')
def view_post(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    comments = post.comments.order_by(Comment.created_at.desc()).all()
    comment_form = CommentForm()
    return render_template('posts/detail.html', post=post, comments=comments, comment_form=comment_form)


@posts_bp.route('/<slug>/comments', methods=['POST'])
@login_required
def add_comment(slug):
    post = Post.query.filter_by(slug=slug, published=True).first_or_404()
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            body=form.body.data.strip(),
            author=current_user,
            post=post
        )
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(error, 'danger')
    return redirect(url_for('posts.view_post', slug=post.slug) + '#comments')


@posts_bp.route('/comments/<int:comment_id>/delete', methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    # Allow comment author OR post author to delete
    if comment.user_id != current_user.id and comment.post.user_id != current_user.id:
        abort(403)
    post_slug = comment.post.slug
    db.session.delete(comment)
    db.session.commit()
    flash('Comment removed successfully.', 'info')
    return redirect(url_for('posts.view_post', slug=post_slug) + '#comments')


@posts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    form = PostForm()
    _populate_category_choices(form)

    if form.validate_on_submit():
        # Auto-generate slug from title if not provided
        raw_slug = form.slug.data.strip() if form.slug.data else form.title.data
        slug = slugify(raw_slug)

        # Ensure slug uniqueness
        base_slug, counter = slug, 1
        while Post.query.filter_by(slug=slug).first():
            slug = f'{base_slug}-{counter}'
            counter += 1

        post = Post(
            title=form.title.data.strip(),
            slug=slug,
            summary=form.summary.data.strip() if form.summary.data else '',
            content=form.content.data,
            published=form.published.data,
            author=current_user,
            category_id=form.category_id.data if form.category_id.data != 0 else None
        )

        # Process tags
        if form.tags.data:
            tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
            for name in tag_names:
                post.tags.append(_get_or_create_tag(name))

        db.session.add(post)
        db.session.commit()
        flash(f'Post "{post.title}" published successfully!', 'success')
        return redirect(url_for('posts.view_post', slug=post.slug))

    return render_template('posts/create.html', form=form, title='New Post')


@posts_bp.route('/<slug>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    if post.author != current_user:
        abort(403)

    form = PostForm(original_slug=post.slug, obj=post)
    _populate_category_choices(form)

    if request.method == 'GET':
        form.tags.data = ', '.join(t.name for t in post.tags)
        form.category_id.data = post.category_id or 0

    if form.validate_on_submit():
        raw_slug = form.slug.data.strip() if form.slug.data else form.title.data
        new_slug = slugify(raw_slug)

        # Ensure uniqueness if slug changed
        if new_slug != post.slug:
            base_slug, counter = new_slug, 1
            while Post.query.filter_by(slug=new_slug).first():
                new_slug = f'{base_slug}-{counter}'
                counter += 1

        post.title = form.title.data.strip()
        post.slug = new_slug
        post.summary = form.summary.data.strip() if form.summary.data else ''
        post.content = form.content.data
        post.published = form.published.data
        post.category_id = form.category_id.data if form.category_id.data != 0 else None

        # Re-process tags
        post.tags.clear()
        if form.tags.data:
            tag_names = [t.strip() for t in form.tags.data.split(',') if t.strip()]
            for name in tag_names:
                post.tags.append(_get_or_create_tag(name))

        db.session.commit()
        flash(f'Post "{post.title}" updated successfully!', 'success')
        return redirect(url_for('posts.view_post', slug=post.slug))

    return render_template('posts/edit.html', form=form, post=post, title=f'Edit: {post.title}')


@posts_bp.route('/<slug>/delete', methods=['POST'])
@login_required
def delete_post(slug):
    post = Post.query.filter_by(slug=slug).first_or_404()
    if post.author != current_user:
        abort(403)
    title = post.title
    db.session.delete(post)
    db.session.commit()
    flash(f'Post "{title}" has been deleted.', 'info')
    return redirect(url_for('posts.list_posts'))
